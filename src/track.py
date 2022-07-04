"""Handles a music track.
"""

import os
from pathlib import Path
import re
import logging as log
import eyed3


class Track:
    """Represents a music track.

    Attributes:
        filepath (Path): Filepath of the track.
        filename (str): Filename of the track.
        eyed3_tags: Tags read and managed by `eyed3`.
        genius_tags: Tags found by `genius`.
        title (str): Title of the track.
        artist (list[str]): Artists of the track.
        main_artist (str): Main artist of the track.
        lyrics (str): Lyrics of the track.
    """

    SPLITTERS = " featuring | feat. | feat | ft. | ft | & | / "

    def __init__(self, filepath: str) -> None:
        self.filepath: Path = filepath
        self.filename: str = os.path.basename(filepath)
        self.eyed3_tags = None
        self.genius_tags = None
        self.title: str = None
        self.artists: list[str] = []
        self.main_artist: str = None
        self.lyrics: str = None

    def read_tags(self) -> bool:
        """Uses eyed3 to read the tags from the file and set them.

        Returns:
            bool: `True` if the tags were successfully read.
        """
        try:
            self.eyed3_tags = eyed3.load(self.filepath).tag
            self.title = self.eyed3_tags.title
            if self.eyed3_tags.artist is not None:
                self.artists = re.split(self.SPLITTERS, self.eyed3_tags.artist)
                self.main_artist = self.artists[0]
        except Exception as exception:
            log.error(
                "Error while reading the tags of file '%s' : %s",
                self.filename,
                str(exception),
            )
            return False
        return True

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

    def save_lyrics(self) -> bool:
        """Saves the lyrics to the file.

        Returns:
            bool: `True` if the lyrics were successfully saved.
        """
        try:
            self.eyed3_tags.lyrics.set(self.lyrics)
            self.eyed3_tags.save(version=eyed3.id3.ID3_V2_3, encoding="utf-8")
        except Exception as exception:
            log.error(
                "Error while saveing the lyrics of file '%s' : %s",
                self.filename,
                str(exception),
            )
            return False
        return True