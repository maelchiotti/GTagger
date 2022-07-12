"""Tools helpful for the GUI.

Includes:
- CustomIcon: Customized implementation of a `QIcon`.
- TrackLayout: Customized implementation of a `QGridLayout` containing the informations of a track.
- Colors: Enumeration of colors.
- States: Enumeration of states.
"""

from __future__ import annotations

import os
import logging as log
from PySide6 import QtCore, QtGui, QtWidgets
from enum import Enum

VERSION = "v1.0.0"
PATH_ICONS = "src/assets/img/icons"


class CustomIcon(QtGui.QIcon):
    """Customized implementation of a `QIcon`.

    Mainly used for the toolbar and the cover placeholder.
    """

    def __init__(
        self, icon_theme: IconTheme, icon_name: str, icon_color: Color_, theme: Theme
    ):
        super().__init__()

        # Construct the icon file path according to the current theme, the icon's theme and the icon's name
        if icon_theme == IconTheme.NORMAL:
            image_path = os.path.join(PATH_ICONS, IconTheme.NORMAL.value, icon_name)
        if icon_theme == IconTheme.OUTLINE:
            icon_name = icon_name + "-" + IconTheme.OUTLINE.value + ".svg"
            image_path = os.path.join(PATH_ICONS, IconTheme.OUTLINE.value, icon_name)
        elif icon_theme == IconTheme.SHARP:
            icon_name = icon_name + "-" + IconTheme.SHARP.value + ".svg"
            image_path = os.path.join(PATH_ICONS, IconTheme.SHARP.value, icon_name)
        if not os.path.exists(image_path):
            log.error("The icon '%s' does not exist", icon_name)
            return
        image = QtGui.QPixmap(image_path)

        # Consruct the icon color according to the the current theme
        color = Color_.get_themed_color(theme, icon_color)

        # Paint the icon with the constructed color
        painter = QtGui.QPainter(image)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.setBrush(QtGui.QColor(color.value))
        painter.setPen(QtGui.QColor(color.value))
        painter.drawRect(image.rect())
        painter.end()

        self.addPixmap(image)


class TrackLayout(QtWidgets.QGridLayout):
    """Customized implementation of a `QGridLayout` containing the informations of a track.

    Signals:
        signal_mouse_event (QtCore.Signal()): Emitted when a mouse event is intercepted.

    Attributes:
        selected (bool): `True` if the track is currently selected.
        covers (dict[Theme, QtGui.QPixmap]): Covers of the track (in dark and light theme).

    Displays:
    - Filename (and filepath as a tooltip)
    - Album cover
    - Title
    - Artists
    - Duration
    - State
    - Lyrics

    Layout:
    ```
    __|    0    |       1      |     2     |
    0 [              filename              ]
    1 [  ...  ]   [ Title    ]   [   ...   ]
    2 [ album ]   [ Artists  ]   [   lyr   ]
    3 [ cover ]   [ Duration ]   [   ics   ]
    4 [  ...  ]   [ State    ]   [   ...   ]
    ```
    """

    signal_mouse_event = QtCore.Signal()

    def __init__(
        self,
        filepath: str,
        filename: str,
        covers: dict[Theme, QtGui.QPixmap],
        duration: str,
        title: str,
        artists: str,
        lyrics: str,
        state: str,
        theme: Theme
    ):
        super().__init__()

        self.selected: bool = False
        self.covers: dict[Theme, QtGui.QPixmap] = covers

        self.label_filename = QtWidgets.QLabel(filename)
        self.label_filename.setToolTip(filepath)
        self.label_cover = QtWidgets.QLabel()
        self.label_cover.setPixmap(self.covers[theme])
        self.label_title = QtWidgets.QLabel(title)
        self.label_artist = QtWidgets.QLabel(artists)
        self.label_duration = QtWidgets.QLabel(duration)
        self.label_state = QtWidgets.QLabel(state)
        self.label_lyrics = QtWidgets.QLabel(lyrics)

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addWidget(self.label_filename, 0, 0, 1, 3)
        self.grid_layout.addWidget(self.label_cover, 1, 0, 4, 1)
        self.grid_layout.addWidget(self.label_title, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.label_artist, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.label_duration, 3, 1, 1, 1)
        self.grid_layout.addWidget(self.label_state, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.label_lyrics, 1, 2, 4, 1)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        self.frame.setLayout(self.grid_layout)
        self.frame.mouseReleaseEvent = self.mouseReleaseEvent

        self.addWidget(self.frame, 0, 0, 1, 1)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Intercepts the mouse release event on the QFrame.

        Enables the user to (de)select a track.

        Args:
            event (QtGui.QMouseEvent): Mouse release event.
        """
        self.selected = not self.selected
        if self.selected:
            color = Color_.black
            background_color = ColorLight.blue
            stylesheet = (
                f"color: {color.value}; background-color: {background_color.value};"
            )
            self.label_cover.setPixmap(self.covers[Theme.LIGHT])
        else:
            stylesheet = ""
            theme: Theme = QtWidgets.QApplication.instance().theme
            self.label_cover.setPixmap(self.covers[theme])
        self.frame.setStyleSheet(stylesheet)

        self.signal_mouse_event.emit()


class Color_(Enum):
    """Enumerates usefull (name, hex) colors."""

    green = "#008000"
    red = "#FF0000"
    blue = "#0000FF"
    orange = "#FFA500"
    grey = "#808080"
    black = "#000000"

    def get_themed_color(theme: Theme, color: Color_) -> ColorDark | ColorLight:
        """Returns the dark of light color corresponding to `color` and depending on `theme`.

        This method is used to retrieve the dark or light color corresponding to a regular color, allowing the application to choose the right color depending on its current theme.

        Args:
            theme (Theme): Current theme of the application.
            color (Color_): Color to return in dark or light.

        Returns:
            ColorDark | ColorLight: Dark or light color corresponding to `color` and depending on `theme`.
        """
        if theme == Theme.DARK:
            return ColorLight.get_color(color.name)
        elif theme == Theme.LIGHT:
            return ColorDark.get_color(color.name)


class ColorDark(Enum):
    """Enumerates usefull (name, hex) dark colors.

    Mainly used for the light theme.
    """

    green = "#006400"
    red = "#8B0000"
    blue = "#00008B"
    orange = "#FF8C00"
    grey = "#696969"

    def get_color(name: str):
        """Returns the color corresponding to `name`.

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

    def get_color(name: str):
        """Returns the color corresponding to `name`.

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
