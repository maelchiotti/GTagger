"""Layout containing the information of a track."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PySide6 import QtCore, QtGui, QtWidgets

from src.consts import COVER_SIZE, LYRICS_LINES, STYLESHEET_QTOOLTIP
from src.enums import CustomColors, State
from src.track import Track

if TYPE_CHECKING:
    from gtagger import GTagger


class StateIndicator(QtWidgets.QWidget):
    """Filled and colored circle indicating the state of a track.

    Attributes:
        x (int): x coordinate.
        y (int): y coordinate.
        w (int): width.
        h (int): height.
    """

    def __init__(
        self, state: State, x: int = 2, y: int = 2, w: int = 15, h: int = 15
    ) -> None:
        """Init StateIndicator.

        Args:
            state (State): State of the track.
            x (int): x coordinate. Defaults to 2.
            y (int): y coordinate. Defaults to 2.
            w (int): width. Defaults to 15.
            h (int): height. Defaults to 15.
        """
        super().__init__()

        self.state: State = state
        self.x: int = x
        self.y: int = y
        self.w: int = w
        self.h: int = h

        self.setFixedWidth(self.x + self.w + 1)
        self.setFixedHeight(self.y + self.h + 1)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Intercept the paint event of the `QWidget`.

        Args:
            event (QtGui.QPaintEvent): Paint event.
        """
        if self.state == State.TAGS_READ:
            color = QtGui.QColor(CustomColors.LIGHT_BLUE.value)
        elif self.state == State.LYRICS_FOUND:
            color = QtGui.QColor(CustomColors.LIGHT_GREEN.value)
        elif self.state == State.LYRICS_NOT_FOUND:
            color = QtGui.QColor(CustomColors.ORANGE.value)
        elif self.state == State.LYRICS_SAVED:
            color = QtGui.QColor(CustomColors.YELLOW_GENIUS.value)
        elif self.state == State.LYRICS_NOT_SAVED:
            color = QtGui.QColor(CustomColors.LIGHT_RED.value)
        else:
            color = QtGui.QColor(CustomColors.LIGHT_GREY.value)

        brush = QtGui.QBrush()
        brush.setColor(color)
        brush.setStyle(QtCore.Qt.SolidPattern)

        pen = QtGui.QPen()
        pen.setColor(CustomColors.GREY.value)
        pen.setStyle(QtCore.Qt.SolidLine)
        pen.setWidth(1)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(self.x, self.y, self.w, self.h)

    def set_state(self, state: State) -> None:
        """Set the state of the indicator to `state` and repaints it.

        Args:
            state (State): New state.
        """
        self.state = state
        self.update()


class TrackLayout(QtWidgets.QFrame):
    """Custom implementation of a `QFrame` containing the information of a track.

    Signals:
        signal_mouse_event (QtCore.Signal): Emitted when a mouse event is intercepted.

    Attributes:
        state (State): State of the track.
        selected (bool): `True` if the track is currently selected.
        cover (QtGui.QPixmap): Cover of the track.
        gtagger (GTagger): GTagger application.
    ```
    """

    signal_mouse_event = QtCore.Signal()

    def __init__(self, track: Track, state: State, gtagger: GTagger) -> None:
        """Init TrackLayout.

        Args:
            track (Track): Track to display.
            state (State): State of the track.
            gtagger (GTagger): GTagger application.
        """
        super().__init__()

        self.state: State = state
        self.selected: bool = False
        self.cover: QtGui.QPixmap = track.cover
        self.gtagger: GTagger = gtagger

        self.setup_ui(track)

    def setup_ui(self, track: Track) -> None:
        """Set up the UI of the window.

        Args:
            track (Track): Track to display.
        """
        self.state_indicator = StateIndicator(self.state)
        self.state_indicator.setToolTip(self.state.value)
        self.label_filename = QtWidgets.QLabel(track.filename)
        self.label_filename.setToolTip(track.get_filepath())
        self.label_cover = QtWidgets.QLabel()
        self.label_cover.setPixmap(track.cover)
        self.label_cover.setFixedWidth(COVER_SIZE)
        self.label_title = QtWidgets.QLabel(track.get_title())
        self.label_title.setToolTip(track.get_title())
        self.label_title.setStyleSheet(
            "QLabel { font-size: 15pt; font-weight: 800; } " + STYLESHEET_QTOOLTIP
        )
        self.label_artists = QtWidgets.QLabel(track.get_artists())
        self.label_artists.setToolTip(track.get_artists())
        self.label_artists.setStyleSheet(
            "QLabel { font-size: 12pt; font-weight: 600; } " + STYLESHEET_QTOOLTIP
        )
        self.label_album = QtWidgets.QLabel(track.get_album())
        self.label_album.setToolTip(track.get_album())
        self.label_album.setStyleSheet(
            "QLabel { font-size: 11pt; font-weight: 400; } " + STYLESHEET_QTOOLTIP
        )
        self.label_duration = QtWidgets.QLabel(f"<i>{track.get_duration()}</i>")
        self.label_duration.setTextFormat(QtCore.Qt.RichText)
        self.label_lyrics = QtWidgets.QLabel(track.get_lyrics(lines=LYRICS_LINES))
        self.label_lyrics.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        self.label_lyrics.setToolTip(track.get_lyrics())
        self.label_lyrics.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
        self.layout_title = QtWidgets.QHBoxLayout()
        self.layout_title.addWidget(self.state_indicator)
        self.layout_title.addWidget(self.label_filename)
        self.layout_title.addStretch()

        if self.state == State.LYRICS_FOUND:
            self.label_lyrics.setStyleSheet(f"color: {CustomColors.LIGHT_GREEN.value}")
        else:
            self.label_lyrics.setStyleSheet("")

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.addLayout(self.layout_title, 0, 0, 1, 2)
        self.layout_.addWidget(self.label_cover, 1, 0, 4, 1)
        self.layout_.addWidget(self.label_title, 1, 1, 1, 1)
        self.layout_.addWidget(self.label_artists, 2, 1, 1, 1)
        self.layout_.addWidget(self.label_album, 3, 1, 1, 1)
        self.layout_.addWidget(self.label_duration, 4, 1, 1, 1)
        self.layout_.addWidget(self.label_lyrics, 0, 2, 5, 1)

        self.setLayout(self.layout_)

        self.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        self.mouseReleaseEvent = self.mouseReleaseEvent

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Intercept the mouse release event on the `QFrame`.

        Enables the user to (de)select a track layout by clicking on it.

        Args:
            event (QtGui.QMouseEvent): Mouse release event.
        """
        # Only take into account the left mouse button
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.toggle_selection()

    def toggle_selection(self, force: Optional[bool] = None) -> None:
        """Toggle the selection of the track layout.

        Args:
            force (Optional[bool]): Force the selection or deselection of the tracks. Has not effect if it is not set. Defaults to None.
        """
        if force is not None:
            self.selected = force
        else:
            self.selected = not self.selected

        if self.selected:
            stylesheet = f"background-color: {CustomColors.DARK_BLUE.value};"
        else:
            stylesheet = ""
        self.setStyleSheet(stylesheet)

        if force is None:
            # Trigger the signal only on a mouse click event, not on key press events
            self.signal_mouse_event.emit()
