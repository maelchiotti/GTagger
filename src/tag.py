"""Manages the tags of a track."""

from __future__ import annotations

import logging as log
import multiprocessing
from pathlib import Path
from typing import TYPE_CHECKING

import genius
from PySide6 import QtCore, QtWidgets

from src.consts import (
    DISCARD_ARTISTS,
    LINES_LYRICS,
    MAX_SEARCH_INDEX,
    MISSING_LYRICS,
    RE_REMOVE_LINES,
    UNWANTED_TITLE_TEXT,
)
from src.enums import State
from src.exceptions import DiscardLyrics
from src.track import Track
from src.track_layout import TrackLayout
from src.tracks_list import CustomListWidgetItem

if TYPE_CHECKING:
    from gtagger import GTagger


class ThreadReadTracks(QtCore.QThread):
    """Reads the tags of the files.

    Signals:
        add_track (object): Emitted when the tags of a file have been read and a track can be added.

    Attributes:
        files (list[Path]): List of files to read.
        gtagger (GTagger): GTagger application.
    """

    add_track = QtCore.Signal(object)

    def __init__(
        self,
        files: list[Path],
        gtagger: GTagger,
    ) -> None:
        """Init ThreadReadTracks.

        Args:
            files (list[Path]): List of files to read.
            gtagger (GTagger): GTagger application.
        """
        super().__init__()
        self.files: list[Path] = files
        self.gtagger: GTagger = gtagger

    def run(self):
        """Run ThreadReadTracks."""
        for file in self.files:
            # Create the track and read its tags
            track = Track(file)
            tags_read = track.read_tags()

            # Signal to WindowMain to skip the track
            if not tags_read:
                self.add_track.emit(None)
                continue

            # Signal to WindowMain to add the track
            self.add_track.emit(track)


class WorkerSearchLyrics(QtCore.QRunnable):
    """Runs the worker for `main_window.search_lyrics()`.

    Uses `SearchLyrics` to search the tracks on Genius and set their lyrics.

    Signals:
        signal_lyrics_searched (): Emitted when the lyrics of a track have been searched.

    Attributes:
        stop_search
        genius (genius.Genius): `wrap-genius` instance.
        overwrite_lyrics (bool): `True` if the lyrics should be overwritten.
        gtagger (GTagger): GTagger application.
    """

    signal_lyrics_searched = QtCore.Signal()

    def __init__(
        self,
        token: str,
        track: Track,
        layout: TrackLayout,
        overwrite_lyrics: bool,
        gtagger: GTagger,
    ) -> None:
        """Init ThreadSearchLyrics.

        Args:
            token (str): Token to search the track on Genius.
            overwrite_lyrics (bool): `True` if the lyrics should be overwritten.
            gtagger (GTagger): GTagger application.
        """
        super().__init__()

        self.stop_search = False
        self.genius: genius.Genius = genius.Genius(token)
        self.track: Track = track
        self.layout: TrackLayout = layout
        self.overwrite_lyrics: bool = overwrite_lyrics
        self.gtagger: GTagger = gtagger

    def run(self):
        """Run ThreadSearchLyrics."""

        if (
            (not self.overwrite_lyrics and self.track.has_lyrics_original())
            or self.track.has_lyrics_new()
            or self.stop_search
        ):
            # self.signal_lyrics_searched.emit()
            return

        found_lyrics = self.search_lyrics()
        if found_lyrics:
            lyrics = self.track.get_lyrics(lines=LINES_LYRICS)
            self.layout.label_lyrics.setText(lyrics)
            self.layout.set_state(State.LYRICS_FOUND)
        else:
            self.layout.set_state(State.LYRICS_NOT_FOUND)
        # self.signal_lyrics_searched.emit()

    def search_lyrics(self) -> bool:
        """Search the lyrics of the track.

        Use `wrap-genius` to search for a track on Genius based on its title and artist, and fetch its lyrics.

        Returns:
            bool: `True` if the lyrics of the track were found.
        """
        if self.track.get_title() == "" or self.track.get_main_artist() == "":
            return False

        # Remove unwanted text from the title that would probably make the search fail
        search_title = self.track.get_title()
        for re_unwanted_text in UNWANTED_TITLE_TEXT:
            search_title = re_unwanted_text.sub("", search_title)
        search_title = search_title.strip()

        # Search for the track
        search = f"{search_title} {self.track.get_main_artist()}"
        try:
            searched_tracks = self.genius.search(search)
        except Exception as exception:
            log.error(
                "Unexpected exception while searching for the track '%s': %s",
                self.track.get_title(),
                exception,
            )
            return False

        for _ in range(MAX_SEARCH_INDEX):
            # Select the next result of the search
            try:
                searched_track = next(searched_tracks)
            except StopIteration:
                log.warning(
                    "Track '%s' by %s not found on Genius",
                    self.track.get_title(),
                    self.track.get_main_artist(),
                )
                return False

            searched_lyrics = searched_track.lyrics
            if not self.check_lyrics(searched_track, searched_lyrics):
                continue

            try:
                self.track.set_lyrics_new(
                    self.format_lyrics(self.track.get_title(), searched_lyrics)
                )
                break
            except DiscardLyrics as exception:
                log.error(exception)
                continue

        return True

    def check_lyrics(
        self, searched_track: genius.api.Song, searched_lyrics: list[str]
    ) -> bool:
        """Check for issues in the lyrics of the track.

        Args:
            searched_track (genius.api.Song): Track that was searched.
            searched_lyrics (list[str]): Lyrics of the track that was searched.

        Returns:
            bool: `True` if the lyrics seem correct.
        """
        # The track's artist indicates it should be discarded
        if searched_track.artist.name in DISCARD_ARTISTS:
            log.error(
                "Discarded the lyrics because the artist was '%s' for the track '%s'",
                searched_track.artist.name,
                self.track.get_title(),
            )
            return False

        # If the lyrics are this long, they are probably wrong
        if len("\n".join(searched_lyrics)) > 15000:
            log.error(
                "Discarded the lyrics because they were too long for the track '%s'",
                self.track.get_title(),
            )
            return False

        # The track's lyrics are missing
        if searched_lyrics[0].startswith(MISSING_LYRICS):
            log.error(
                "Discarded the lyrics because they were missing for the track '%s'",
                self.track.get_title(),
            )
            return False

        return True

    @staticmethod
    def format_lyrics(title: str, unformatted_lyrics: list[str]) -> str:
        """Format `unformatted_lyrics` by removing unwanted text.

        Args:
            title (str): Title of the track.
            unformatted_lyrics (list[str]): Lyrics to format.

        Returns:
            str: Formatted lyrics.

        Raises:
            DiscardLyrics: If the lyrics should be discarded.
        """
        for index, line in enumerate(unformatted_lyrics):
            if len(line) > 500:
                # If the line is this long, the lyrics are probably wrong
                raise DiscardLyrics("a line was too long", title, len(line))
            if line.startswith("[") and line.endswith("]"):
                # Remove indications such as [Chorus]
                unformatted_lyrics[index] = ""
            else:
                unformatted_lyrics[index] = line.strip()
        lyrics = "\n".join(unformatted_lyrics)
        lyrics = RE_REMOVE_LINES.sub("\n\n", lyrics)
        lyrics = lyrics.strip()
        return lyrics
