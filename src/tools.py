"""Tools helpful for the GUI.

The tools include:
- Colors: enumeration of colors.
- States: enumeration of states.
"""

from enum import Enum

VERSION = "v1.0.0"
PATH_ICONS = "src/assets/img/icons"

class Colors(Enum):
    """Enumerates usefull (name, hex code) colors."""

    lightgreen = "#AED9B2"
    lightred = "#FF7F7F"


class States(Enum):
    """Enumerates the different states of the application."""

    TAGS_READ = "Tags read"
    TAGS_NOT_READ = "Couldn't read tags"
    LYRICS_FOUND = "Lyrics found"
    LYRICS_NOT_FOUND = "Couldn't find lyrics"
    LYRICS_SAVED = "Lyrics saved"
    LYRICS_NOT_SAVED = "Couldn't save the lyrics"


class Themes(Enum):
    LIGHT = "light"
    DARK = "dark"