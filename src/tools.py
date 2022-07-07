"""Tools helpful for the GUI.

The tools include:
- Colors: enumeration of colors.
- States: enumeration of states.
"""

from enum import Enum

VERSION = "v1.0.0"
PATH_ICONS = "src/assets/img/icons"


class Color_(Enum):
    """Enumerates usefull (name, hex code) colors."""

    green = "green"  # todo
    red = "red"  # todo
    blue = "blue"  # todo
    orange = "orange"  # todo
    grey = "grey"  # todo


class ColorDark(Enum):
    green = "#006400"
    red = "#8B0000"
    blue = "#00008B"
    orange = "#FF8C00"
    grey = "#696969"

    def get_color(name):
        return ColorDark.__getitem__(name)
    

class ColorLight(Enum):
    green = "#90EE90"
    red = "#F08080"
    blue = "#00008B"  # todo
    orange = "#FF8C00"  # todo
    grey = "#696969"  # todo

    def get_color(name):
        return ColorLight.__getitem__(name)


class State(Enum):
    """Enumerates the different states of the application."""

    TAGS_READ = "Tags read"
    TAGS_NOT_READ = "Couldn't read tags"
    LYRICS_FOUND = "Lyrics found"
    LYRICS_NOT_FOUND = "Couldn't find lyrics"
    LYRICS_SAVED = "Lyrics saved"
    LYRICS_NOT_SAVED = "Couldn't save the lyrics"


class Theme(Enum):
    LIGHT = "light"
    DARK = "dark"


class IconTheme(Enum):
    NORMAL = "normal"
    OUTLINE = "outline"
    SHARP = "sharp"
