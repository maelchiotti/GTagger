"""Tools helpful for the GUI.

The tools include:
- Colors: enumeration of colors.
- States: enumeration of states.
"""

from enum import Enum

VERSION = "v1.0.0"
PATH_ICONS = "src/assets/img/icons"


class Color_(Enum):
    """Enumerates usefull (name, hex) colors."""

    green = "#008000"
    red = "#FF0000"
    blue = "#0000FF"
    orange = "#FFA500"
    grey = "#808080"


class ColorDark(Enum):
    """Enumerates usefull (name, hex) dark colors.
    
    Mainly used for the light theme.
    """
    green = "#006400"
    red = "#8B0000"
    blue = "#00008B"
    orange = "#FF8C00"
    grey = "#696969"

    def get_color(name):
        """Returns the color corresponding to `name`.
        
        This method is used to retrieve the dark color corresponding to a regular color, allowing the application to choose the right color depending on its current theme.

        Args:
            name (str): Name of the color to return.

        Returns:
            ColorDark: Dark color named `name`.
        """
        return ColorDark.__getitem__(name)
    

class ColorLight(Enum):
    """Enumerates usefull (name, hex) light colors.
    
    Mainly used for the dark theme.
    """
    green = "#90EE90"
    red = "#F08080"
    blue = "#ADD8E6"
    orange = "#FFFACD"
    grey = "#D3D3D3"

    def get_color(name):
        """Returns the color corresponding to `name`.
        
        This method is used to retrieve the light color corresponding to a regular color, allowing the application to choose the right color depending on its current theme.

        Args:
            name (str): Name of the color to return.

        Returns:
            ColorLight: Light color named `name`.
        """
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
    """Enumerates the different themes of the application.
    
    Includes:
    - Dark
    - Light
    """
    DARK = "dark"
    LIGHT = "light"


class IconTheme(Enum):
    """Enumerates the different themes of the icons.
    
    Includes:
    - Normal
    - Outline (shape is not filled)
    - Sharp (shape's angles are sharper)
    """
    NORMAL = "normal"
    OUTLINE = "outline"
    SHARP = "sharp"
