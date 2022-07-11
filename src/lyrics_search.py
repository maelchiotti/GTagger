"""Searches a track's lyrics on Genius.
"""

import re
import logging as log
import lyricsgenius
from lyricsgenius import types

from src.track import Track


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

        lyrics = self.format_lyrics(searched_track.lyrics)
        track.lyrics = lyrics
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
