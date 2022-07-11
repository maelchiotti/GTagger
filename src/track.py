"""Handles a music track.
"""

import os
from pathlib import Path
import re
import logging as log
import time
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
        self.eyed3_infos = None
        self.eyed3_tags = None
        self.genius_tags = None
        self.duration: float = None
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
            eyed3_load = eyed3.load(self.filepath)
            self.eyed3_infos = eyed3_load.info
            self.eyed3_tags = eyed3_load.tag
            self.duration = self.eyed3_infos.time_secs
            self.title = self.eyed3_tags.title
            if self.eyed3_tags.artist is not None:
                self.artists = re.split(self.SPLITTERS, self.eyed3_tags.artist)
                self.main_artist = self.artists[0]
            if len(self.eyed3_tags.lyrics) > 0:
                self.lyrics = self.eyed3_tags.lyrics[0].text
        except Exception as exception:
            log.error(
                "Error while reading the tags of file '%s' : %s",
                self.filename,
                str(exception),
            )
            return False
        return True
    
    def get_duration(self) -> str:
        if self.duration is None:
            return "??:??"
        else:
            duration = time.gmtime(round(self.duration))
            return time.strftime("%M:%S", duration)

    def get_title(self) -> str:
        """Returns the title of the track, or "No title" if the artist is not set.

        Returns:
            str: Title of the track.
        """
        if self.title is None or self.title == "":
            return "No title"
        else:
            return self.title
    
    def get_artists(self) -> str:
        """Returns the artists of the track, or "No artist(s)" if the artists are not set.

        Returns:
            str: Artists of the track.
        """
        if not self.artists:
            return "No artist(s)"
        else:
            return ", ".join(self.artists)
    
    def get_main_artist(self) -> str:
        """Returns the main artist of the track, or "No artist" if the main artist is not set.

        Returns:
            str: Main artist of the track.
        """
        if self.main_artist is None or self.main_artist == "":
            return "No artist"
        else:
            return self.main_artist

    def get_lyrics(self, length: int = 100) -> str:
        """Returns the lyrics of the track up to `length` characters.

        Args:
            length (int): Maximum number of characters to return (default is 100).

        Returns:
            str: Lyrics up to `length`.
        """
        if self.lyrics is None:
            return "No lyrics"
        else:            
            return self.lyrics.get()[:length]

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
                "Error while saving the lyrics of file '%s' : %s",
                self.filename,
                str(exception),
            )
            return False
        return True
