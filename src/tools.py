"""Tools helpful for the GUI.

Includes:
- CustomIcon: Customized implementation of a `QIcon`.
- TrackLayout: Customized implementation of a `QGridLayout` containing the informations of a track.
- Color_: Enumeration of normal colors.
- ColorDark: Enumeration of light colors for the dark theme.
- ColorLight: Enumeration of dark colors for the light theme.
- State: Enumeration of states.
- Theme: Enumeration of application themes.
- IconTheme: Enumeration of icon themes.
"""

from __future__ import annotations

import os
import logging as log
import sys
from PySide6 import QtCore, QtGui, QtWidgets
from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GTagger
    from src.track import Track

VERSION = "v1.2.0"
ICONS_PATH = "src/assets/img/icons"
TOKEN_URL = QtCore.QUrl("https://genius.com/api-clients")


class CustomIcon(QtGui.QIcon):
    """Customized implementation of a `QIcon`.

    Allows to use a custom `.svg` icon with a custom color.
    """

    def __init__(
        self, icon_theme: IconTheme, icon_name: str, icon_color: Color_, theme: Theme
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


class TrackLayout(QtWidgets.QGridLayout):
    """Customized implementation of a `QGridLayout` containing the informations of a track.

    Signals:
        signal_mouse_event (QtCore.Signal): Emitted when a mouse event is intercepted.

    Attributes:
        selected (bool): `True` if the track is currently selected.
        covers (dict[tuple[Theme, Mode], QtGui.QPixmap]): Covers of the track (in dark and light theme).

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
    __|    0   |      1     |     2    |
    0 [ (state) filename               ]
    1 [  ...  ] [ Title    ] [ ...     ]
    2 [ album ] [ Artists  ] [ lyr     ]
    3 [ cover ] [ Album    ] [ ics     ]
    4 [  ...  ] [ Duration ] [ ...     ]
    ```
    """

    signal_mouse_event = QtCore.Signal()

    def __init__(self, track: Track, state: State, gtagger: GTagger) -> None:
        super().__init__()

        self.state: State = state
        self.gtagger: GTagger = gtagger

        self.selected: bool = False
        self.covers: dict[tuple[Theme, Mode], QtGui.QPixmap] = track.covers

        if self.gtagger.mode == Mode.NORMAL:
            self.setup_normal_mode(track)
        elif self.gtagger.mode == Mode.COMPACT:
            self.setup_compact_mode(track)

    def setup_normal_mode(self, track: Track):
        """Sets up the layout as normal mode.

        Args:
            track (Track): Track containing the informations to display.
        """
        self.state_indicator = StateIndicator(self.state)
        self.state_indicator.setToolTip(self.state.value)
        self.label_filename = QtWidgets.QLabel(track.filename)
        self.label_filename.setToolTip(track.get_filepath())
        self.label_cover = QtWidgets.QLabel()
        self.label_cover.setPixmap(self.covers[(self.gtagger.theme, self.gtagger.mode)])
        self.label_cover.setFixedWidth(COVER_SIZE[self.gtagger.mode])
        self.label_title = QtWidgets.QLabel(track.get_title())
        self.label_title.setStyleSheet("font-size: 15pt; font-weight:800;")
        self.label_artists = QtWidgets.QLabel(track.get_artists())
        self.label_artists.setStyleSheet("font-size: 12pt; font-weight:600;")
        self.label_album = QtWidgets.QLabel(track.get_album())
        self.label_album.setStyleSheet("font-size: 11pt; font-weight:400;")
        self.label_duration = QtWidgets.QLabel(f"<i>{track.get_duration()}</i>")
        self.label_duration.setTextFormat(QtCore.Qt.RichText)
        self.label_lyrics = QtWidgets.QLabel(
            track.get_lyrics(lines=LYRICS_LINES[self.gtagger.mode])
        )
        self.label_lyrics.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.label_lyrics.setToolTip(track.get_lyrics())

        self.layout_title = QtWidgets.QHBoxLayout()
        self.layout_title.addWidget(self.state_indicator)
        self.layout_title.addWidget(self.label_filename)
        self.layout_title.addStretch()

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addLayout(self.layout_title, 0, 0, 1, 3)
        self.grid_layout.addWidget(self.label_cover, 1, 0, 4, 1)
        self.grid_layout.addWidget(self.label_title, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.label_artists, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.label_album, 3, 1, 1, 1)
        self.grid_layout.addWidget(self.label_duration, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.label_lyrics, 1, 2, 4, 1)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        self.frame.setLayout(self.grid_layout)
        self.frame.mouseReleaseEvent = self.mouseReleaseEvent
        self.frame.resizeEvent = self.resizeEvent

        self.addWidget(self.frame, 0, 0, 1, 1)

    def setup_compact_mode(self, track: Track):
        """Sets up the layout as compact mode.

        Args:
            track (Track): Track containing the informations to display.
        """
        self.state_indicator = StateIndicator(self.state)
        self.state_indicator.setToolTip(self.state.value)
        self.label_cover = QtWidgets.QLabel()
        self.label_cover.setPixmap(self.covers[(self.gtagger.theme, self.gtagger.mode)])
        self.label_cover.setFixedWidth(COVER_SIZE[self.gtagger.mode])
        self.label_title = QtWidgets.QLabel(track.get_title())
        self.label_title.setStyleSheet("font-size: 15pt; font-weight:800;")
        self.label_artists = QtWidgets.QLabel(track.get_artists())
        self.label_artists.setStyleSheet("font-size: 12pt; font-weight:600;")
        self.label_lyrics = QtWidgets.QLabel(
            track.get_lyrics(lines=LYRICS_LINES[self.gtagger.mode])
        )
        self.label_lyrics.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.label_lyrics.setToolTip(track.get_lyrics())

        self.layout_title = QtWidgets.QHBoxLayout()
        self.layout_title.addWidget(self.state_indicator)
        self.layout_title.addWidget(self.label_title)
        self.layout_title.addStretch()

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addWidget(self.label_cover, 0, 0, 2, 1)
        self.grid_layout.addLayout(self.layout_title, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.label_artists, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.label_lyrics, 0, 2, 2, 1)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        self.frame.setLayout(self.grid_layout)
        self.frame.mouseReleaseEvent = self.mouseReleaseEvent
        self.frame.resizeEvent = self.resizeEvent

        self.addWidget(self.frame, 0, 0, 1, 1)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Intercepts the mouse release event on the `QFrame`.

        Enables the user to (de)select a track.

        Args:
            event (QtGui.QMouseEvent): Mouse release event.
        """
        # Only take into account the left mouse button
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.selected = not self.selected
        if self.selected:
            color = Color_.black
            background_color = ColorLight.blue
            stylesheet = (
                f"color: {color.value}; background-color: {background_color.value};"
            )
            self.label_cover.setPixmap(self.covers[(Theme.LIGHT, self.gtagger.mode)])
        else:
            stylesheet = ""
            self.label_cover.setPixmap(
                self.covers[(self.gtagger.theme, self.gtagger.mode)]
            )
        self.frame.setStyleSheet(stylesheet)

        self.signal_mouse_event.emit()

    def resizeEvent(self, newSize: QtGui.QResizeEvent):
        """Intercepts the resize event on the `QFrame`.

        Args:
            newSize (QtGui.QResizeEvent): Resize event.
        """
        self.label_artists.setFixedWidth(round(0.33 * newSize.size().width()))


class StateIndicator(QtWidgets.QWidget):
    """Filled and colored circle indicating the state of a track."""

    def __init__(
        self, state: State, x: int = 2, y: int = 2, w: int = 15, h: int = 15
    ) -> None:
        super().__init__()

        self.state: State = state
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Intercepts the paint event of the `QWidget`.

        Args:
            event (QtGui.QPaintEvent): Paint event.
        """
        if self.state == State.TAGS_READ:
            color = QtGui.QColor(ColorLight.blue.value)
        elif self.state == State.LYRICS_FOUND:
            color = QtGui.QColor(ColorLight.green.value)
        elif self.state == State.LYRICS_NOT_FOUND:
            color = QtGui.QColor(Color_.orange.value)
        elif self.state == State.LYRICS_SAVED:
            color = QtGui.QColor(Color_.yellow_genius.value)
        elif self.state == State.LYRICS_NOT_SAVED:
            color = QtGui.QColor(ColorLight.red.value)

        brush = QtGui.QBrush()
        brush.setColor(color)
        brush.setStyle(QtCore.Qt.SolidPattern)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(brush)
        painter.drawEllipse(self.x, self.y, self.w, self.h)

        self.setFixedWidth(self.x + self.w)
        self.setFixedHeight(self.y + self.h)

    def set_state(self, state: State) -> None:
        """Sets the state of the indicator to `state` and repaints it.

        Args:
            state (State): New state.
        """
        self.state = state
        self.update()


class Settings(Enum):
    """Enumerates the settings of the application."""

    THEME = "theme"
    MODE = "mode"
    RECUSRIVE_SEARCH = "recursive_search"
    OVERWRITE_LYRICS = "overwrite_lyrics"


class Color_(Enum):
    """Enumerates usefull (name, hex) colors."""

    green = "#008000"
    red = "#FF0000"
    blue = "#0000FF"
    orange = "#FFA500"
    grey = "#808080"
    yellow = "#FFFF00"

    yellow_genius = "#FFFF64"
    black = "#000000"

    @staticmethod
    def get_themed_color(theme: Theme, color: Color_) -> ColorDark | ColorLight:
        """Returns the dark of light color corresponding to `color` and depending on `theme`.

        Allows to retrieve the dark or light color corresponding to a regular color,
        allowing the application to choose the right color depending on its current theme.

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
        else:
            return ColorDark.black


class ColorDark(Enum):
    """Enumerates usefull (name, hex) dark colors."""

    green = "#006400"
    red = "#8B0000"
    blue = "#00008B"
    orange = "#FF8C00"
    grey = "#696969"
    yellow = "#DAA520"

    black = "#000000"

    @staticmethod
    def get_color(name: str) -> ColorDark:
        """Returns the color corresponding to `name`.

        Args:
            name (str): Name of the color to return.

        Returns:
            ColorDark: Dark color named `name`.
        """
        return ColorDark.__getitem__(name)


class ColorLight(Enum):
    """Enumerates usefull (name, hex) light colors."""

    green = "#90EE90"
    red = "#F08080"
    blue = "#ADD8E6"
    orange = "#FFFACD"
    grey = "#D3D3D3"
    yellow = "#FFFF64"

    black = "#000000"

    @staticmethod
    def get_color(name: str) -> ColorLight:
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

    @staticmethod
    def get_theme(value: str) -> Theme:
        """Returns the `Theme` corresponding to `value`.

        Args:
            value (str): Value of the theme.

        Returns:
            Theme: Theme corresponding to `value`.
        """
        return Theme.__getitem__(value.upper())


class IconTheme(Enum):
    """Enumerates the different themes of the icons.

    Includes:
    - Normal
    - Outline: shape is not filled)
    - Sharp: shape's angles are sharper)
    """

    NORMAL = "normal"
    OUTLINE = "outline"
    SHARP = "sharp"


class Mode(Enum):
    """Enumerates the different layout modes of the track layout.

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


COVER_SIZE = {Mode.NORMAL: 128, Mode.COMPACT: 32}
LYRICS_LINES = {Mode.NORMAL: 8, Mode.COMPACT: 2}
