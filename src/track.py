"""Handles a music track."""

import os
from pathlib import Path
import re
import logging as log
import time
import eyed3
from eyed3.core import Tag, AudioInfo
from eyed3.id3.frames import ImageFrame
from PySide6 import QtCore, QtGui

from src.tools import COVER_SIZE, CustomIcon, Color_, IconTheme, Mode, Theme


class Track(QtCore.QObject):
    """Represents a music track.

    Signals:
        signal_lyrics_changed (QtCore.Signal): Emmited when the lyrics of the track are changed.

    Attributes:
        filepath (Path): Filepath of the track.
        filename (str): Filename of the track.
        eyed3_infos (AudioInfo): Informations read by `eyed3`.
        eyed3_tags (Tag): Tags read and managed by `eyed3`.
        genius_tags: Tags found by `genius`.
        duration (float): Duration of the track in seconds.
        covers (dict[tuple[Theme, Mode], QtGui.QPixmap]): Covers of the track (in dark and light theme and in normal and compact mode).
        title (str): Title of the track.
        artists (list[str]): Artists of the track.
        main_artist (str): Main artist of the track.
        album (str): Album of the track.
        lyrics_new (str): New lyrics of the track.
    """

    SPLITTERS = " featuring | feat. | feat | ft. | ft | & | / "

    signal_lyrics_changed = QtCore.Signal()

    def __init__(self, filepath: Path) -> None:
        super().__init__()

        self.filepath: Path = filepath
        self.filename: str = os.path.basename(filepath)
        self.eyed3_infos: AudioInfo = None
        self.eyed3_tags: Tag = None
        self.genius_tags = None
        self.duration: float = 0.0
        self.covers: dict[tuple[Theme, Mode], QtGui.QPixmap] = {}
        self.title: str = ""
        self.artists: list[str] = []
        self.main_artist: str = ""
        self.album: str = ""
        self.lyrics_new: str = ""

    def read_tags(self) -> bool:
        """Uses eyed3 to read the tags from the file and sets them.

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
                cover_normal = cover.scaled(COVER_SIZE[Mode.NORMAL], COVER_SIZE[Mode.NORMAL], QtCore.Qt.KeepAspectRatio)
                self.covers[(Theme.DARK, Mode.NORMAL)] = cover_normal
                self.covers[(Theme.LIGHT, Mode.NORMAL)] = cover_normal
                cover_compact = cover.scaled(COVER_SIZE[Mode.COMPACT], COVER_SIZE[Mode.COMPACT], QtCore.Qt.KeepAspectRatio)
                self.covers[(Theme.DARK, Mode.COMPACT)] = cover_compact
                self.covers[(Theme.LIGHT, Mode.COMPACT)] = cover_compact
            else:
                # If the track doesn't have a cover, build two placeholders
                icon_dark: CustomIcon = CustomIcon(
                    IconTheme.OUTLINE, "image", Color_.grey, Theme.DARK
                )
                cover_dark = icon_dark.pixmap(
                    icon_dark.actualSize(QtCore.QSize(COVER_SIZE[Mode.NORMAL], COVER_SIZE[Mode.NORMAL]))
                )
                cover_dark_normal = cover_dark.scaled(
                    COVER_SIZE[Mode.NORMAL], COVER_SIZE[Mode.NORMAL], QtCore.Qt.KeepAspectRatio
                )
                cover_dark_compact = cover_dark.scaled(
                    COVER_SIZE[Mode.COMPACT], COVER_SIZE[Mode.COMPACT], QtCore.Qt.KeepAspectRatio
                )
                self.covers[(Theme.DARK, Mode.NORMAL)] = cover_dark_normal
                self.covers[(Theme.DARK, Mode.COMPACT)] = cover_dark_compact
                
                icon_light: CustomIcon = CustomIcon(
                    IconTheme.OUTLINE, "image", Color_.grey, Theme.LIGHT
                )
                cover_light = icon_light.pixmap(
                    icon_light.actualSize(QtCore.QSize(COVER_SIZE[Mode.NORMAL], COVER_SIZE[Mode.NORMAL]))
                )
                cover_light_normal = cover_light.scaled(
                    COVER_SIZE[Mode.NORMAL], COVER_SIZE[Mode.NORMAL], QtCore.Qt.KeepAspectRatio
                )
                cover_light_compact = cover_light.scaled(
                    COVER_SIZE[Mode.COMPACT], COVER_SIZE[Mode.COMPACT], QtCore.Qt.KeepAspectRatio
                )
                self.covers[(Theme.LIGHT, Mode.NORMAL)] = cover_light_normal
                self.covers[(Theme.LIGHT, Mode.COMPACT)] = cover_light_compact
            self.title = self.eyed3_tags.title
            if self.eyed3_tags.artist is not None:
                self.artists = re.split(self.SPLITTERS, self.eyed3_tags.artist)
                self.main_artist = self.artists[0]
            self.album = self.eyed3_tags.album
        except Exception as exception:
            log.error(
                "Error while reading the tags of file '%s' : %s",
                self.filename,
                str(exception),
            )
            return False
        return True

    def get_filepath(self) -> str:
        """Returns the path to the file.

        Converting to a string is needed because the type of `filepath`
        changes according to the OS.

        Returns:
            str: Path to the file.
        """
        return str(self.filepath)

    def get_duration(self) -> str:
        """Returns the formatted duration of the track.

        The duration is rounded to the second and returned in the format `MM:SS`.

        Returns:
            str: Formatted duration of the track
        """
        duration = time.gmtime(round(self.duration))
        return time.strftime("%M:%S", duration)

    def get_title(self) -> str:
        """Returns the title of the track, or "No title" if the artist is not set.

        Returns:
            str: Title of the track.
        """
        if self.title == "":
            return "No title"
        else:
            return self.title

    def get_artists(self) -> str:
        """Returns the artists of the track, or "No artist(s)" if the artists are not set.

        Returns:
            str: Artists of the track.
        """
        if len(self.artists) == 0:
            return "No artist(s)"
        else:
            return ", ".join(self.artists)

    def get_main_artist(self) -> str:
        """Returns the main artist of the track, or "No artist" if the main artist is not set.

        Returns:
            str: Main artist of the track.
        """
        if self.main_artist == "":
            return "No artist"
        else:
            return self.main_artist

    def get_album(self) -> str:
        """Returns the album of the track, or "No album" if the album is not set.

        Returns:
            str: Album of the track.
        """
        if self.album == "":
            return "No album"
        else:
            return self.album

    def get_lyrics(self, lines: int = None, length: int = None) -> str:
        """Returns the lyrics of the track, or "No lyrics" if the lyrics are not set.

        Returns `new_lyrics` is they are set, otherwise the original ones read by `eyeD3`.

        If specified, returns a maximum of `lines` lines.
        Otherwise, if specified, returns a maximum of `length` characters.
        In any other case, returns the full lyrics.

        Args:
            lines (int): Maximum number of lines to return. Defaults to `None`.
            length (int): Maximum number of characters to return. Defaults to `None`.

        Returns:
            str: Lyrics of the track (up to `lines`, `length` or full).
        """
        if self.lyrics_new is not None:
            lyrics = self.lyrics_new
        elif self.has_lyrics_original():
            lyrics = self.eyed3_tags.lyrics[0].text
        else:
            return "No lyrics"

        if lines is not None:
            lyrics_split = lyrics.split("\n")
            return "\n".join(lyrics_split[:lines])
        elif length is not None:
            return lyrics[:length]
        else:
            return lyrics

    def get_lyrics_original(self) -> str:
        """Returns the original lyrics of the track read by `eyeD3`,
        or "No lyrics" if the lyrics are not set.

        Returns:
            str: Original lyrics of the track.
        """
        if self.has_lyrics_original():
            return self.eyed3_tags.lyrics[0].text
        else:
            return "No lyrics"

    def set_lyrics(self, lyrics: str):
        """Sets the lyrics of the track to `lyrics`.

        Also emits a signal indicating that the lyrics have changed.

        Args:
            lyrics (str): New lyrics of the track.
        """
        self.lyrics_new = lyrics
        self.signal_lyrics_changed.emit()

    def save_lyrics(self) -> bool:
        """Saves the lyrics to the file.

        Returns:
            bool: `True` if the lyrics were successfully saved.
        """
        if self.lyrics_new is not None:
            try:
                self.eyed3_tags.lyrics.set(self.lyrics_new)
                self.eyed3_tags.save(version=eyed3.id3.ID3_V2_3, encoding="utf-8")
            except Exception as exception:
                log.error(
                    "Error while saving the lyrics of file '%s' : %s",
                    self.filename,
                    str(exception),
                )
                return False
        return True

    def has_lyrics_original(self) -> bool:
        """Returns `True` if the track has original lyrics read by `eyeD3`.

        Returns:
            bool: `True` if the track has original lyrics.
        """
        return len(self.eyed3_tags.lyrics) > 0
