"""Searches a track's lyrics on Genius."""

from __future__ import annotations

import re
import logging as log
import lyricsgenius
from lyricsgenius import types
import genius
from PySide6 import QtCore

from src.tools import LYRICS_LINES, State, TrackLayout
from src.track import Track


class TrackSearch:
    """Allows to search a track on Genius.

    Attributes:
        token (str): Genius client access token.
        genius (genius.Genius): `genius` instance.
    """

    def __init__(self, token: str) -> None:
        search = re.search("[^a-zA-Z0-9_-]", token)
        if search is not None:
            log.error("Incorrect access token: %s", search)
            self.token: str = None
            self.genius: genius.Genius = None
        else:
            self.token: str = token
            self.genius: genius.Genius = genius.Genius(access_token=self.token)

    def search_track(self, track: Track) -> bool:
        """Searches for a track on Genius using the `track.title` and the `track.artist`.

        The tags found are added to the `genius_tags` attribute of `track`.

        Args:
            track (Track): Track to search.

        Returns:
            bool: `True` is the track was found.
        """
        if track.title is None or track.main_artist is None:
            return False
        search = f"{track.title} {track.main_artist}"
        try:
            searched_tracks = self.genius.search(search)
        except Exception as exception:
            log.error("Unexpected exception: %s", exception)
            return False
        try:
            searched_track = next(searched_tracks)
        except StopIteration:
            log.warning(
                "Track '%s' by %s not found on Genius", track.title, track.main_artist
            )
            return False
        track.genius_tags = searched_track
        return True


class LyricsSearch:
    """Allows to search a track's lyrics on Genius.

    Attributes:
        token (str): Genius client access token.
        lyrics_genius (lyricsgenius.Genius): `lyrics_genius` instance.
    """

    def __init__(self, token: str) -> None:
        self.token: str = token
        self.lyrics_genius: lyricsgenius.Genius = lyricsgenius.Genius(
            access_token=self.token, verbose=False, remove_section_headers=True
        )

    def search_lyrics(self, track: Track) -> bool:
        """Searches for a track's lyrics on Genius.

        The lyrics are added to the `lyrics` attribute.

        Args:
            track (Track): Track for which the lyrics will be searched.

        Returns:
            bool: ̀`True` if the lyrics were found.
        """
        if track.genius_tags is None:
            return False

        searched_track: types.Song = None
        while True:
            try:
                searched_track = self.lyrics_genius.search_song(
                    song_id=track.genius_tags.id, get_full_info=False
                )
                break
            except Exception as exception:
                log.error("Unexpected exception: %s", exception)
                return False

        if searched_track is None:
            log.warning(
                "Track '%s' lyrics by %s not found on Genius",
                track.title,
                track.main_artist,
            )
            return False

        track.set_lyrics(self.format_lyrics(searched_track.lyrics))
        return True

    @staticmethod
    def format_lyrics(unformatted_lyrics: str) -> str:
        """Formats `unformatted_lyrics` by removing unwanted text.

        Args:
            unformatted_lyrics (str): Lyrics to format.

        Returns:
            str: Formatted lyrics.
        """
        lines = unformatted_lyrics.split("\n")
        if len(lines) > 0:
            lines.pop(0)
        if len(lines) > 1:
            lines[len(lines) - 1] = re.sub("[0-9]+Embed", "", lines[len(lines) - 1])
        return "\n".join(lines)


class ThreadLyricsSearch(QtCore.QThread):
    """Runs the thread for `main_window.search_lyrics()`.

    Uses `TrackSearch` to search the tracks on Genius,
    and `LyricsSearch` to search and set their lyrics.

    Attributes:
        token (str): Token to search the track on Genius.
        track_layouts (dict[Track, TrackLayout]): Layouts of the tracks.
    """

    def __init__(self, token: str, track_layouts: dict[Track, TrackLayout]) -> None:
        super().__init__()

        self.token: str = token
        self.track_layouts: dict[Track, TrackLayout] = track_layouts

    def run(self):
        for track, track_layout in self.track_layouts.copy().items():
            track_search = TrackSearch(self.token)
            track_search.search_track(track)
            lyrics_search = LyricsSearch(self.token)
            found_lyrics = lyrics_search.search_lyrics(track)
            if found_lyrics:
                lyrics = track.get_lyrics(lines=LYRICS_LINES)
                track_layout.label_lyrics.setText(lyrics)
                track_layout.label_lyrics.setToolTip(track.get_lyrics_original())
                track_layout.label_state.setText(State.LYRICS_FOUND.value)
            else:
                track_layout.label_state.setText(State.LYRICS_NOT_FOUND.value)
