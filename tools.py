"""Tools helpful for the GUI.

The tools include:
- Track: a music track.
- TrackSearch: search a track on Genius.
- LyricsSearch: search a track's lyrics on Genius.
- Tools: miscellaneous tools.
"""

import os
import re
import logging as log
import eyed3
import genius
import lyricsgenius
from lyricsgenius import types


class Track:
    """Represents a music track.

    Attributes:
        filepath (str): Filepath of the track.
        filename (str): Filename of the track.
        genius_tags (classes.Song): Tags found by `genius`.
        title (str): Title of the track.
        artist (list[str]): Artists of the track.
        main_artist (str): Main artist of the track.
        lyrics (str): Lyrics of the track.
    """

    SPLITTERS = " featuring | feat. | feat | ft. | ft | & | / "

    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.filename: str = os.path.basename(filepath)
        self.genius_tags = None
        self.title: str = None
        self.artists: list[str] = []
        self.main_artist: str = None
        self.lyrics: str = None
        self.read_tags()

    def read_tags(self) -> None:
        """Uses eyed3 to read the tags from the file and set them.
        """
        tags = eyed3.load(self.filepath)
        self.title = tags.tag.title
        if tags.tag.artist is not None:
            self.artists = re.split(self.SPLITTERS, tags.tag.artist)
            self.main_artist = self.artists[0]

    def get_lyrics(self, length: int) -> str:
        """Returns the lyrics up to `length` characters.

        Args:
            length (int): Maximum number of characters to return.

        Returns:
            str: Lyrics up to `length`.
        """
        if self.lyrics is None:
            return ""
        return self.lyrics[:length]


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
        """
        Searches for a track on Genius
        """
        # todo if one is none
        search = track.title + " " + track.main_artist
        searched_tracks = self.genius.search(search)
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

        lyrics = Tools.format_lyrics(searched_track.lyrics)
        track.lyrics = lyrics
        return True


class Tools:
    """Contains miscellaneous tools.
    
    Attributes:
        COLORS (dict[str, str]): list of (name: hex value) colors 
    """

    COLORS = {"lightgreen": "#AED9B2", "lightred": "#FF7F7F"}

    @staticmethod
    def format_lyrics(unformatted_lyrics: str) -> str:
        """Formats the lyrics by removing unwanted text.

        Args:
            unformatted_lyrics (str): Lyrics to format.

        Returns:
            str: _description_
        """
        lines = unformatted_lyrics.split("\n")
        if len(lines) > 0:
            lines.pop(0)
        if len(lines) > 1:
            lines[len(lines) - 1] = re.sub("[0-9]+Embed", "", lines[len(lines) - 1])
        return "\n".join(lines)
