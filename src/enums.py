"""Enumerations."""

from __future__ import annotations

from enum import Enum


class Settings(Enum):
    """Enumerates the settings of the application."""

    RECURSIVE_SEARCH = "recursive_search"
    OVERWRITE_LYRICS = "overwrite_lyrics"
    TOOLBAR_POSITION = "toolbar_position"


class CustomColors(Enum):
    """Enumerates useful (name = #hex) colors."""

    LIGHT_GREEN = "#90EE90"
    LIGHT_RED = "#F08080"
    LIGHT_BLUE = "#ADD8E6"
    LIGHT_ORANGE = "#FFFACD"
    LIGHT_GREY = "#D3D3D3"

    RED = "#FF0000"
    ORANGE = "#FFA500"
    GREY = "#808080"

    DARK_BLUE = "#2B3C4F"
    DARK_GREY = "#202124"

    YELLOW_GENIUS = "#FFFF64"
    BLACK = "#000000"


class State(Enum):
    """Enumerates the different states of the application."""

    TAGS_READ = "Tags read"
    TAGS_NOT_READ = "Couldn't read tags"
    LYRICS_FOUND = "Lyrics found"
    LYRICS_NOT_FOUND = "Couldn't find lyrics"
    LYRICS_SAVED = "Lyrics saved"
    LYRICS_NOT_SAVED = "Couldn't save the lyrics"


class FileType(Enum):
    """Enumerates the different file types supported by GTagger."""

    MP3 = "mp3"
    FLAC = "flac"
    NOT_SUPPORTED = "not supported"


class Sort(Enum):
    """Enumerates the different sorting modes for the list of tracks."""

    DESCENDING = "descending"
    ASCENDING = "ascending"
