"""Enumerations."""

from __future__ import annotations

from enum import Enum


class Settings(Enum):
    """Enumerates the settings of the application."""

    RECURSIVE_SEARCH = "recursive_search"
    OVERWRITE_LYRICS = "overwrite_lyrics"


class Color_(Enum):
    """Enumerates useful (name = #hex) colors."""

    light_green = "#90EE90"
    light_red = "#F08080"
    light_blue = "#ADD8E6"
    light_orange = "#FFFACD"
    light_grey = "#D3D3D3"

    red = "#FF0000"
    orange = "#FFA500"
    grey = "#808080"

    dark_blue = "#2B3C4F"
    dark_grey = "#202124"

    yellow_genius = "#FFFF64"
    black = "#000000"


class State(Enum):
    """Enumerates the different states of the application."""

    TAGS_READ = "Tags read"
    TAGS_NOT_READ = "Couldn't read tags"
    LYRICS_FOUND = "Lyrics found"
    LYRICS_NOT_FOUND = "Couldn't find lyrics"
    LYRICS_SAVED = "Lyrics saved"
    LYRICS_NOT_SAVED = "Couldn't save the lyrics"


class FileType(Enum):
    """Enumerates the different file types supported by GTagger.

    Includes:
        - FLAC
        - MP3
        - NOT_SUPPORTED
    """

    MP3 = "mp3"
    FLAC = "flac"
    NOT_SUPPORTED = "not supported"
