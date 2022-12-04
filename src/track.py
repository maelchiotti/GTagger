"""Handles a music track."""

import logging as log
import os
import re
import time
from pathlib import Path
from typing import Optional, Union

import mutagen
from mutagen.flac import Picture as FLACPicture
from mutagen.flac import StreamInfo as FLACInfo
from mutagen.id3._frames import APIC as MP3Picture
from mutagen.id3._frames import USLT
from mutagen.mp3 import MPEGInfo as MP3Info
from PySide6 import QtCore, QtGui

from src.utils import COVER_SIZE, SPLITTERS, Color_, FileType, Mode, get_icon


class Track(QtCore.QObject):
    """Represents a music track.

    Signals:
        signal_lyrics_changed (QtCore.Signal): Emitted when the lyrics of the track are changed.

    Attributes:
        filepath (Path): Filepath of the track.
        filename (str): Filename of the track.
        covers (dict[Mode, QtGui.QPixmap]): Covers of the track
        (in dark and light theme and in normal and compact mode).
        artists (list[str]): Artists of the track.
        main_artist (str): Main artist of the track.
        lyrics_new (str): New lyrics of the track.
        self.file (mutagen.FileType): File read by `mutagen`, containing tags and metadata.
    """

    signal_lyrics_changed = QtCore.Signal()

    def __init__(self, filepath: Path) -> None:
        super().__init__()

        self.filepath: Path = filepath
        self.filename: str = os.path.basename(filepath)
        self.covers: dict[Mode, QtGui.QPixmap] = {}
        self.artists: list[str] = []
        self.main_artist: str = ""
        self.lyrics_new: str = ""
        self.file: mutagen.FileType = None

    def read_tags(self) -> bool:
        """Uses mutagen to read the tags from the file and sets them.

        Returns:
            bool: `True` if the tags were successfully read.
        """
        # File: tags and infos
        try:
            self.file = mutagen.File(self.filepath)
        except Exception as exception:
            log.error(
                "Error while opening the file '%s' : %s",
                self.filename,
                str(exception),
            )
            return False

        try:
            # Covers
            if self.has_pictures():
                # The track has a cover
                picture: FLACPicture = self.get_picture()
                cover = QtGui.QPixmap()
                cover.loadFromData(picture.data)
            else:
                # The track doesn't have a cover, build the placeholders
                icon_dark: QtGui.QIcon = get_icon(
                    "image-off", color=Color_.light_grey.value
                )
                cover = icon_dark.pixmap(
                    icon_dark.actualSize(QtCore.QSize(COVER_SIZE, COVER_SIZE))
                )
            cover_normal = cover.scaled(
                COVER_SIZE,
                COVER_SIZE,
                QtCore.Qt.KeepAspectRatio,
            )
            cover_compact = cover.scaled(
                COVER_SIZE,
                COVER_SIZE,
                QtCore.Qt.KeepAspectRatio,
            )
            self.covers = cover_normal
            self.covers = cover_compact

            # Artists: all and main
            if self.get_file_type() == FileType.FLAC:
                if "artist" in self.file.tags:
                    self.artists = re.split(SPLITTERS, self.file.tags["artist"][0])
                    self.main_artist = self.artists[0]
            else:
                if self.file.tags is not None and self.file.tags["TPE1"] is not None:
                    self.artists = re.split(SPLITTERS, self.file.tags["TPE1"].text[0])
                    self.main_artist = self.artists[0]
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

        Returns:
            str: Path to the file.
        """
        return self.filepath.as_posix()

    def get_duration(self) -> str:
        """Returns the formatted duration of the track.

        The duration is rounded to the second and returned in the format `MM:SS`.

        Returns:
            str: Formatted duration of the track
        """
        duration = time.gmtime(round(self.file.info.length))
        return time.strftime("%M:%S", duration)

    def get_title(self) -> str:
        """Returns the title of the track, or "No title" if the title is not set.

        Returns:
            str: Title of the track.
        """
        if self.get_file_type() == FileType.FLAC:
            if "title" in self.file.tags:
                return self.file.tags["title"][0]
            else:
                return "No title"
        else:
            if self.file.tags is not None and "TIT2" in self.file.tags:
                return self.file.tags["TIT2"].text[0]
            else:
                return "No title"

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
        if self.get_file_type() == FileType.FLAC:
            if "album" in self.file.tags:
                return self.file.tags["album"][0]
            else:
                return "No album"
        else:
            if self.file.tags is not None and "TALB" in self.file.tags:
                return self.file.tags["TALB"].text[0]
            else:
                return "No album"

    def get_picture(self) -> Union[FLACPicture, MP3Picture]:
        """Returns the first picture of the track.

        Returns:
            FLACPicture | MP3Picture: Picture of the track.
        """
        if self.get_file_type() == FileType.FLAC:
            return self.file.pictures[0]
        else:
            return self.file.tags["APIC:"]

    def has_pictures(self) -> bool:
        """Returns `True` if the track has pictures.

        Returns:
            bool: `True` if the track has pictures.
        """
        if self.get_file_type() == FileType.FLAC:
            return len(self.file.pictures) > 0
        else:
            return self.file.tags is not None and "APIC:" in self.file.tags

    def get_file_type(self) -> FileType:
        """Returns the type of the file.

        Returns:
            FileType: Type of the file.
        """
        if isinstance(self.file.info, FLACInfo):
            return FileType.FLAC
        elif isinstance(self.file.info, MP3Info):
            return FileType.MP3
        else:
            return FileType.NOT_SUPPORTED

    def get_lyrics(
        self, lines: Optional[int] = None, length: Optional[int] = None
    ) -> str:
        """Returns the lyrics of the track, or "No lyrics" if the lyrics are not set.

        Returns `new_lyrics` is they are set, otherwise the original ones read by `mutagen`.

        If specified, returns a maximum of `lines` lines.
        Otherwise, if specified, returns a maximum of `length` characters.
        In any other case, returns the full lyrics.

        Args:
            lines (int): Maximum number of lines to return. Defaults to `None`.
            length (int): Maximum number of characters to return. Defaults to `None`.

        Returns:
            str: Lyrics of the track (up to `lines`, `length` or full).
        """
        if self.lyrics_new != "":
            lyrics = self.lyrics_new
        elif self.has_lyrics_original():
            lyrics = self.get_lyrics_original()
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
        """Returns the original lyrics of the track read by `mutagen`,
        or "No lyrics" if the lyrics are not set.

        Returns:
            str: Original lyrics of the track.
        """
        if self.has_lyrics_original():
            if self.get_file_type() == FileType.FLAC:
                return self.file.tags["lyrics"][0]
            else:
                return self.get_uslt().text
        else:
            return "No lyrics"

    def set_lyrics_new(self, lyrics: str):
        """Sets the lyrics of the track to `lyrics`.

        Also emits a signal indicating that the lyrics have changed.

        Args:
            lyrics (str): New lyrics of the track.
        """
        lyrics = lyrics.strip("\n")
        self.lyrics_new = lyrics
        self.signal_lyrics_changed.emit()

    def save_lyrics(self) -> bool:
        """Saves the lyrics to the file.

        Returns:
            bool: `True` if the lyrics were successfully saved.
        """
        if self.has_lyrics_new():
            try:
                if self.get_file_type() == FileType.FLAC:
                    self.file.tags["lyrics"] = self.lyrics_new
                else:
                    self.file.tags.add(USLT(text=self.lyrics_new))
                self.file.save()
            except Exception as exception:
                log.error(
                    "Error while saving the lyrics of file '%s' : %s",
                    self.filename,
                    str(exception),
                )
                return False
        return True

    def has_lyrics_original(self) -> bool:
        """Returns `True` if the track has original lyrics read by `mutagen`.

        Returns:
            bool: `True` if the track has original lyrics.
        """
        if self.get_file_type() == FileType.FLAC:
            return "lyrics" in self.file.tags and len(self.file.tags["lyrics"]) > 0
        else:
            return (
                self.file.tags is not None
                and self.get_uslt() is not None
                and len(self.get_uslt().text) > 0
            )

    def has_lyrics_new(self) -> bool:
        """Returns `True` if the track has new lyrics.

        Returns:
            bool: `True` if the track has new lyrics.
        """
        return self.lyrics_new != ""

    def get_uslt(self) -> Union[USLT, None]:
        """Returns the USLT field of a MP3 file.

        In ID3 tags of a MP3 file, lyrics are stored in a field named "USLT::XXX",
        where "XXX" stands for a code identifying the language of the lyrics
        (ex: "eng" for english lyrics). This code can also be missing, and then
        "XXX" is used instead. This function searches for the first tag beginning
        with "USLT", no matter the language.

        Returns:
            USLT | None: USLT field of a MP3 file.
        """
        for name, tag in self.file.tags.items():
            if "USLT" in name:
                return tag
        return None
