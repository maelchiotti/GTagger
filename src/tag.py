"""Manages the tags of a track.

Includes:
- `ThreadTrackRead`: Reads the tags of a track.
- `LyricsSearch`: Searches a track ant its lyrics on Genius.
- `ThreadLyricsSearch`: Runs the lyrics search.
"""

from __future__ import annotations

import logging as log
from pathlib import Path
from typing import TYPE_CHECKING

import genius
from PySide6 import QtCore, QtGui, QtWidgets

from src.track import Track
from src.track_layout import TrackLayout
from src.utils import (
    DISCARD_ARTISTS,
    LYRICS_LINES,
    MISSING_LYRICS,
    RE_REMOVE_LINES,
    UNWANTED_TITLE_TEXT,
    DiscardLyrics,
    State,
)

if TYPE_CHECKING:
    from gtagger import GTagger


class ThreadTrackRead(QtCore.QThread):
    """Reads the tags of the files.

    Signals:
        add_track (QtCore.Signal(object)): Emitted when the tags of a file
        have been read and a track can be added.

    Attributes:
        files (list[Path]): List of files to read.
        action_add_files (QtGui.QAction): Add files action.
        action_add_folder (QtGui.QAction): Add folder action.
        gtagger (GTagger): GTagger application.
    """

    add_track = QtCore.Signal(object)

    def __init__(
        self,
        files: list[Path],
        action_add_files: QtGui.QAction,
        action_add_folder: QtGui.QAction,
        gtagger: GTagger,
    ) -> None:
        super().__init__()
        self.files: list[Path] = files
        self.action_add_files: QtGui.QAction = action_add_files
        self.action_add_folder: QtGui.QAction = action_add_folder
        self.gtagger: GTagger = gtagger

    def run(self):
        self.action_add_files.setEnabled(False)
        self.action_add_folder.setEnabled(False)
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
        self.action_add_files.setEnabled(True)
        self.action_add_folder.setEnabled(True)


class LyricsSearch(QtCore.QObject):
    """Searches for the lyrics of a track.

    Attributes:
        token (str): Genius client access token.
        genius (genius.Genius): `wrap-genius` instance.
    """

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token: str = token
        self.genius: genius.Genius = genius.Genius(self.token)

    def search_lyrics(self, track: Track) -> bool:
        """Uses `wrap-genius` to search a track on Genius
        based on its title and artist, and fetch its lyrics.

        Args:
            track (Track): Track for which to search the lyrics.

        Returns:
            bool: `True` if the lyrics of the track were found.
        """
        if track.get_title() == "" or track.get_main_artist() == "":
            return False

        # Remove unwanted text from the title that would probably make the search fail
        search_title = track.get_title()
        for re_unwanted_text in UNWANTED_TITLE_TEXT:
            search_title = re_unwanted_text.sub("", search_title)
        search_title = search_title.strip()

        search = f"{search_title} {track.get_main_artist()}"
        print(search)
        try:
            searched_tracks = self.genius.search(search)
        except Exception as exception:
            log.error(
                "Unexpected exception while searching for the track '%s': %s",
                track.get_title(),
                exception,
            )
            return False

        try:
            searched_track = next(searched_tracks)
        except StopIteration:
            log.warning(
                "Track '%s' by %s not found on Genius",
                track.get_title(),
                track.get_main_artist(),
            )
            return False

        print(searched_track.artist.id)
        if searched_track.artist.name in DISCARD_ARTISTS:
            # The track's artist indicates it should be discarded
            log.error(
                "Discarded the lyrics because the artist was '%s' for the track '%s'",
                searched_track.artist.name,
                track.get_title(),
            )
            return False

        searched_lyrics = searched_track.lyrics

        if len("\n".join(searched_lyrics)) > 15000:
            # If the lyrics are this long, they are probably wrong
            log.error(
                "Discarded the lyrics because they were too long for the track '%s'",
                track.get_title(),
            )
            return False

        if searched_lyrics[0].startswith(MISSING_LYRICS):
            # The track's lyrics are missing
            log.error(
                "Discarded the lyrics because they were missing for the track '%s'",
                track.get_title(),
            )
            return False

        try:
            track.set_lyrics_new(self.format_lyrics(track.get_title(), searched_lyrics))
        except DiscardLyrics as exception:
            log.error(exception)
            return False

        return True

    @staticmethod
    def format_lyrics(title: str, unformatted_lyrics: list[str]) -> str:
        """Formats `unformatted_lyrics` by removing unwanted text.

        Args:
            unformatted_lyrics (list[str]): Lyrics to format.

        Returns:
            str: Formatted lyrics.
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


class ThreadSearchLyrics(QtCore.QThread):
    """Runs the thread for `main_window.search_lyrics()`.

    Uses `SearchLyrics` to search the tracks on Genius and set their lyrics.

    Signals:
        signal_lyrics_searched (QtCore.Signal): Emitted when the lyrics of a track
        have been searched.

    Attributes:
        token (str): Token to search the track on Genius.
        track_layouts (dict[Track, TrackLayout]): Layouts of the tracks.
        overwrite_lyrics (bool): `True` if the lyrics should be overwritten.
        button_stop_search (QtWidgets.QPushButton): Button to stop the search.
        gtagger (GTagger): GTagger application.
    """

    signal_lyrics_searched = QtCore.Signal()

    def __init__(
        self,
        token: str,
        track_layouts_items: dict[Track, tuple[TrackLayout, QtWidgets.QListWidgetItem]],
        overwrite_lyrics: bool,
        button_stop_search: QtWidgets.QPushButton,
        gtagger: GTagger,
    ) -> None:
        super().__init__()

        self.stop_search = False

        self.token: str = token
        self.track_layouts_items: dict[
            Track, tuple[TrackLayout, QtWidgets.QListWidgetItem]
        ] = track_layouts_items
        self.overwrite_lyrics: bool = overwrite_lyrics
        self.button_stop_search: QtWidgets.QPushButton = button_stop_search
        self.gtagger: GTagger = gtagger

    def run(self):
        self.button_stop_search.setEnabled(True)
        lyrics_search = LyricsSearch(self.token)
        for track, layout_item in self.track_layouts_items.copy().items():
            layout = layout_item[0]
            if (
                (not self.overwrite_lyrics and track.has_lyrics_original())
                or track.has_lyrics_new()
                or self.stop_search
            ):
                self.signal_lyrics_searched.emit()
                continue

            found_lyrics = lyrics_search.search_lyrics(track)
            if found_lyrics:
                lyrics = track.get_lyrics(lines=LYRICS_LINES[self.gtagger.mode])
                layout.label_lyrics.setText(lyrics)
                layout.label_lyrics.setToolTip(track.get_lyrics())
                layout.state_indicator.set_state(State.LYRICS_FOUND)
                layout.state_indicator.setToolTip(State.LYRICS_FOUND.value)
                layout.state = State.LYRICS_FOUND
            else:
                layout.state_indicator.set_state(State.LYRICS_NOT_FOUND)
                layout.state_indicator.setToolTip(State.LYRICS_NOT_FOUND.value)
                layout.state = State.LYRICS_NOT_FOUND
            self.signal_lyrics_searched.emit()
        self.button_stop_search.setEnabled(False)
