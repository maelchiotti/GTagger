"""Tools helpful for the GUI.

Includes:
- SettingsManager: Handles the settings.
- CustomIcon: Customized implementation of a `QIcon`.
- Settings: Enumeration of settings.
- Color_: Enumeration of colors.
- State: Enumeration of states.
- IconTheme: Enumeration of icon themes.
"""

from __future__ import annotations

import os
import logging as log
import sys
from typing import Any
from PySide6 import QtCore, QtGui
from enum import Enum

VERSION = "v1.2.0"
ICONS_PATH = "src/assets/img/icons"
TOKEN_URL = QtCore.QUrl("https://genius.com/api-clients")


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
        self, setting: str, default: Any = None, type: object = None
    ) -> Any:
        """Returns the value of the setting `setting`.

        The setting is defaulted to `default` if it does not exist,
        which defaults to `None`.

        `type` specifies the type of the data to return,
        it has to be a native data type.

        Args:
            setting (str): Name of the setting.
            default (Any, optional): Default value for the setting. Defaults to `None`.
            type (object, optional): Type of the setting. Defaults to `None`.

        Returns:
            Any: Value of the setting.
        """
        if type is None:
            return self.settings.value(setting, defaultValue=default)
        else:
            return self.settings.value(setting, defaultValue=default, type=type)

    def set_setting(self, setting: str, value: object) -> None:
        """Sets the value of `setting` to `value`.

        Args:
            setting (str): Name of the setting.
            value (object): Value of the setting.
        """
        self.settings.setValue(setting, value)


class CustomIcon(QtGui.QIcon):
    """Customized implementation of a `QIcon`.

    Allows to use a custom `.svg` icon with a custom color.
    """

    def __init__(
        self, icon_theme: IconTheme, icon_name: str, icon_color: Color_
    ) -> None:
        super().__init__()

        # Construct the icon file path according to the current theme,
        # the icon's theme and the icon's name.
        # The images are retrieved from the ressource folder when using an executable,
        # or from the assets folder when running from source.
        if icon_theme == IconTheme.NORMAL:
            icon_name = icon_name + ".svg"
            image_name = os.path.join(IconTheme.NORMAL.value, icon_name)
            image_path = self.add_resource_path(image_name)
            if not os.path.exists(image_path):
                image_path = os.path.join(ICONS_PATH, image_name)
        if icon_theme == IconTheme.OUTLINE:
            icon_name = icon_name + "-" + IconTheme.OUTLINE.value + ".svg"
            image_name = os.path.join(IconTheme.OUTLINE.value, icon_name)
            image_path = self.add_resource_path(image_name)
            if not os.path.exists(image_path):
                image_path = os.path.join(ICONS_PATH, image_name)
        elif icon_theme == IconTheme.SHARP:
            icon_name = icon_name + "-" + IconTheme.SHARP.value + ".svg"
            image_name = os.path.join(IconTheme.SHARP.value, icon_name)
            image_path = self.add_resource_path(image_name)
            if not os.path.exists(image_path):
                image_path = os.path.join(ICONS_PATH, image_name)

        if not os.path.exists(image_path):
            log.error("The icon '%s' at '%s' does not exist", icon_name, image_path)
            return
        image = QtGui.QPixmap(image_path)

        # Paint the icon with the constructed color
        painter = QtGui.QPainter(image)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.setBrush(QtGui.QColor(icon_color.value))
        painter.setPen(QtGui.QColor(icon_color.value))
        painter.drawRect(image.rect())
        painter.end()

        self.addPixmap(image)

    @staticmethod
    def add_resource_path(ressource: str) -> str:
        """Returns the final path to the application's ressource `ressource`.

        The ressources are stored in a special folder by the OS
        when extracted from the executable, which path is appended
        before the relative path to ressource.

        Args:
            relative_path (str): Relative path to the ressource.

        Returns:
            str: Path to the ressource.
        """
        if hasattr(sys, "_MEIPASS"):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, ressource)


class Settings(Enum):
    """Enumerates the settings of the application."""

    MODE = "mode"
    RECUSRIVE_SEARCH = "recursive_search"
    OVERWRITE_LYRICS = "overwrite_lyrics"


class Color_(Enum):
    """Enumerates usefull (name = #hex) colors."""

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


class IconTheme(Enum):
    """Enumerates the different themes of the icons.

    Includes:
    - Normal
    - Outline: shape is not filled
    - Sharp: shape's angles are sharper
    """

    NORMAL = "normal"
    OUTLINE = "outline"
    SHARP = "sharp"


class Mode(Enum):
    """Enumerates the different layout modes of a track layout.

    Includes:
    - Normal: normal layout with all informations
    - Compact: compact layout with only important informations
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
