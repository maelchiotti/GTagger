"""Handles a music track.
"""

import os
from pathlib import Path
import re
import logging as log
import time
import eyed3
from eyed3.core import Tag, AudioInfo
from eyed3.id3.frames import ImageFrame
from PySide6 import QtCore, QtGui, QtWidgets

from src.tools import CustomIcon, Color_, IconTheme, Theme


class Track:
    """Represents a music track.

    Attributes:
        filepath (Path): Filepath of the track.
        filename (str): Filename of the track.
        eyed3_infos (AudioInfo): Informations read by `eyed3`.
        eyed3_tags (Tag): Tags read and managed by `eyed3`.
        genius_tags: Tags found by `genius`.
        covers (dict[Theme, QtGui.QPixmap]): Covers of the track (in dark and light theme).
        title (str): Title of the track.
        artist (list[str]): Artists of the track.
        main_artist (str): Main artist of the track.
        lyrics (str): Lyrics of the track.
    """

    SPLITTERS = " featuring | feat. | feat | ft. | ft | & | / "

    def __init__(self, filepath: str) -> None:
        self.filepath: Path = filepath
        self.filename: str = os.path.basename(filepath)
        self.eyed3_infos: AudioInfo = None
        self.eyed3_tags: Tag = None
        self.genius_tags = None
        self.duration: float = None
        self.covers: dict[Theme, QtGui.QPixmap] = {Theme.DARK: None, Theme.LIGHT: None}
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
            if eyed3_load.info is None:
                return False
            self.eyed3_tags = eyed3_load.tag
            self.duration = self.eyed3_infos.time_secs
            if len(self.eyed3_tags.images) > 0:
                image: ImageFrame = self.eyed3_tags.images[0]
                cover = QtGui.QPixmap()
                cover.loadFromData(image.image_data)
                cover = cover.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
                self.covers[Theme.DARK] = cover
                self.covers[Theme.LIGHT] = cover
            else:        
                icon_dark: CustomIcon = CustomIcon(IconTheme.OUTLINE, "image", Color_.grey, Theme.DARK)
                cover_dark = icon_dark.pixmap(icon_dark.actualSize(QtCore.QSize(128, 128)))
                cover_dark = cover_dark.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
                icon_light: CustomIcon = CustomIcon(IconTheme.OUTLINE, "image", Color_.grey, Theme.LIGHT)
                cover_light = icon_light.pixmap(icon_light.actualSize(QtCore.QSize(128, 128)))
                cover_light = cover_light.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
                self.covers[Theme.DARK] = cover_dark
                self.covers[Theme.LIGHT] = cover_light
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

    def create_cover_placeholder(self, theme: Theme) -> None:
        if len(self.eyed3_tags.images) > 0:
            return


    def get_filepath(self) -> str:
        return str(self.filepath)

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

    def get_lyrics(self, lines: int = None, length: int = None) -> str:
        """Returns the lyrics of the track.

        If specified, returns a maximum of `lines` lines.
        Otherwise, if specified, returns a maximum of `length` characters.
        In any other case, returns the full lyrics.

        Args:
            lines (int): Maximum number of lines to return (defaults to `None`).
            length (int): Maximum number of characters to return (defaults to `None`).

        Returns:
            str: Lyrics (up to `lines`, `length` or full).
        """
        if self.lyrics is None:
            return "No lyrics"
        else:
            if lines is not None:
                lyrics = self.lyrics.split("\n")
                return "\n".join(lyrics[:lines])
            elif length is not None:
                return self.lyrics[:length]
            else:
                return self.lyrics

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
