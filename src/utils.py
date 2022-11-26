"""Tools helpful for the GUI.

Includes:
- `SettingsManager`: Handles the settings.
- `Settings`: Enumeration of settings.
- `Color_`: Enumeration of colors.
- `State`: Enumeration of states.
- `get_icon()`: Returns an icon.
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Any

from PySide6 import QtCore, QtGui
from qtawesome import icon

VERSION = "v1.2.2"
TOKEN_URL = QtCore.QUrl("https://genius.com/api-clients")
SPLITTERS = " featuring | feat. | feat | ft. | ft | & | / "
UNWANTED_TITLE_TEXT = [
    re.compile(r"\(radio\)", re.IGNORECASE),
    re.compile(r"\(radio edit\)", re.IGNORECASE),
    re.compile(r"\(live\)", re.IGNORECASE),
    re.compile(r"\(live version\)", re.IGNORECASE),
    re.compile(r"\(alternative\)", re.IGNORECASE),
    re.compile(r"\(alternative version\)", re.IGNORECASE),
    re.compile(r"\(extended\)", re.IGNORECASE),
    re.compile(r"\(extended version\)", re.IGNORECASE),
]
RE_REMOVE_LINES = re.compile(r"\n{2,}")


class SettingsManager(QtCore.QObject):
    """Settings manager that handles of the settings of the application.

    Attributes:
        settings (QtCore.QSettings): Settings of the application.
    """

    def __init__(self) -> None:
        super().__init__()

        QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)
        self.settings = QtCore.QSettings()

    def get_setting(
        self, setting: str, default: Any = None, type_: object = None
    ) -> Any:
        """Returns the value of the setting `setting`.

        The setting is defaulted to `default` if it does not exist,
        which defaults to `None`.

        `type` specifies the type of the data to return,
        it has to be a native data type.

        Args:
            setting (str): Name of the setting.
            default (Any, optional): Default value for the setting. Defaults to `None`.
            type_ (object, optional): Type of the setting. Defaults to `None`.

        Returns:
            Any: Value of the setting.
        """
        if type_ is None:
            return self.settings.value(setting, defaultValue=default)
        else:
            return self.settings.value(setting, defaultValue=default, type=type_)

    def set_setting(self, setting: str, value: object) -> None:
        """Sets the value of `setting` to `value`.

        Args:
            setting (str): Name of the setting.
            value (object): Value of the setting.
        """
        self.settings.setValue(setting, value)


class Settings(Enum):
    """Enumerates the settings of the application."""

    MODE = "mode"
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


class Mode(Enum):
    """Enumerates the different layout modes of a track layout.

    Includes:
    - Normal: normal layout with all information
    - Compact: compact layout with only important information
    """

    NORMAL = "normal"
    COMPACT = "compact"

    @staticmethod
    def get_mode(value: str) -> Mode:
        """Returns the `Mode` corresponding to `value`.

        Args:
            value (str): Value of the mode.

        Returns:
            Mode: Mode corresponding to `value`.
        """
        return Mode.__getitem__(value.upper())


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


def get_icon(
    name: str, active: str = None, color: str = "white", color_active: str = "white"
) -> QtGui.QIcon:
    """Returns the MDI6 icon `name` as a `QIcon`.

    Args:
        name (str): Name of the MDI6 icon.
        active (str, optional): Name of the MDI6 icon when the button is active. Defaults to None.
        color (str, optional): Color of the icon. Defaults to "white".
        color_active (str, optional): Color of the icon when the button is active. Defaults to "white".

    Returns:
        QtGui.QIcon: MDI6 icon `name` as a `QIcon`.
    """
    name = f"mdi6.{name}"
    if active is None:
        active = name
    return icon(name, active=active, color=color, color_active=color_active)


# Sizes of the covers depending on the mode
COVER_SIZE = {
    Mode.NORMAL: 128,
    Mode.COMPACT: 64,
}

# Number of lyrics lines to display depending on the mode
LYRICS_LINES = {
    Mode.NORMAL: 9,
    Mode.COMPACT: 4,
}
