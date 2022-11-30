"""Layout containing the information of a track."""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from PySide6 import QtCore, QtGui, QtWidgets

from src.track import Track
from src.utils import COVER_SIZE, LYRICS_LINES, STYLESHEET_QTOOLTIP, Color_, Mode, State

if TYPE_CHECKING:
    from gtagger import GTagger


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

        self.setFixedWidth(self.x + self.w + 1)
        self.setFixedHeight(self.y + self.h + 1)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        """Intercepts the paint event of the `QWidget`.

        Args:
            event (QtGui.QPaintEvent): Paint event.
        """
        if self.state == State.TAGS_READ:
            color = QtGui.QColor(Color_.light_blue.value)
        elif self.state == State.LYRICS_FOUND:
            color = QtGui.QColor(Color_.light_green.value)
        elif self.state == State.LYRICS_NOT_FOUND:
            color = QtGui.QColor(Color_.orange.value)
        elif self.state == State.LYRICS_SAVED:
            color = QtGui.QColor(Color_.yellow_genius.value)
        elif self.state == State.LYRICS_NOT_SAVED:
            color = QtGui.QColor(Color_.light_red.value)

        brush = QtGui.QBrush()
        brush.setColor(color)
        brush.setStyle(QtCore.Qt.SolidPattern)

        pen = QtGui.QPen()
        pen.setColor(Color_.grey.value)
        pen.setStyle(QtCore.Qt.SolidLine)
        pen.setWidth(1)

        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawEllipse(self.x, self.y, self.w, self.h)

    def set_state(self, state: State) -> None:
        """Sets the state of the indicator to `state` and repaints it.

        Args:
            state (State): New state.
        """
        self.state = state
        self.update()


class TrackLayout(QtWidgets.QWidget):
    """Customized implementation of a `QWidget` containing the information of a track.

    Signals:
        signal_mouse_event (QtCore.Signal): Emitted when a mouse event is intercepted.

    Attributes:
        selected (bool): `True` if the track is currently selected.
        covers (dict[tuple[Theme, Mode], QtGui.QPixmap]): Covers of the track
        (in dark and light theme).

    Displays:
    - Filename (and filepath as a tooltip)
    - Album cover
    - Title
    - Artists
    - Duration
    - State
    - Lyrics

    Layouts:
    - Normal:
    ```
    __|    0   |      1     |     2    |
    0 [ (state) filename     [ ...     ]
    1 [  ...  ] [ Title    ] [ ly      ]
    2 [ album ] [ Artists  ] [ ri      ]
    3 [ cover ] [ Album    ] [ cs      ]
    4 [  ...  ] [ Duration ] [ ...     ]
    ```
    - Compact:
    ```
    __|    0   |      1          |     2    |
    1 [ album ] [ (state) Title ] [ lyr     ]
    2 [ cover ] [ Artists       ] [ ics     ]
    ```
    """

    signal_mouse_event = QtCore.Signal()

    def __init__(self, track: Track, state: State, gtagger: GTagger) -> None:
        super().__init__()

        self.state: State = state
        self.gtagger: GTagger = gtagger

        self.selected: bool = False
        self.covers: dict[Mode, QtGui.QPixmap] = track.covers

        self.setup_ui(track)

    def setup_ui(self, track: Track) -> None:
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.addWidget(self.build_normal_ui(track))
        self.stacked_widget.addWidget(self.build_compact_ui(track))

        self.frame_layout = QtWidgets.QHBoxLayout()
        self.frame_layout.addWidget(self.stacked_widget)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        self.frame.mouseReleaseEvent = self.mouseReleaseEvent
        self.frame.setLayout(self.frame_layout)
        self.switch_layout()

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.frame, 0, 0, 1, 1)

        self.setLayout(self.layout_)

    def build_normal_ui(self, track: Track) -> QtWidgets.QWidget:
        """Sets up the layout as normal mode.

        Args:
            track (Track): Track containing the information to display.
        """
        state_indicator = StateIndicator(self.state)
        state_indicator.setToolTip(self.state.value)
        label_filename = QtWidgets.QLabel(track.filename)
        label_filename.setToolTip(track.get_filepath())
        label_cover = QtWidgets.QLabel()
        label_cover.setPixmap(self.covers[Mode.NORMAL])
        label_cover.setFixedWidth(COVER_SIZE[Mode.NORMAL])
        label_title = QtWidgets.QLabel(track.get_title())
        label_title.setToolTip(track.get_title())
        label_title.setStyleSheet(
            "QLabel { font-size: 15pt; font-weight: 800; } " + STYLESHEET_QTOOLTIP
        )
        label_artists = QtWidgets.QLabel(track.get_artists())
        label_artists.setToolTip(track.get_artists())
        label_artists.setStyleSheet(
            "QLabel { font-size: 12pt; font-weight: 600; } " + STYLESHEET_QTOOLTIP
        )
        label_album = QtWidgets.QLabel(track.get_album())
        label_album.setToolTip(track.get_album())
        label_album.setStyleSheet(
            "QLabel { font-size: 11pt; font-weight: 400; } " + STYLESHEET_QTOOLTIP
        )
        label_duration = QtWidgets.QLabel(f"<i>{track.get_duration()}</i>")
        label_duration.setTextFormat(QtCore.Qt.RichText)
        label_lyrics = QtWidgets.QLabel(
            track.get_lyrics(lines=LYRICS_LINES[Mode.NORMAL])
        )
        label_lyrics.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        label_lyrics.setToolTip(track.get_lyrics())
        label_lyrics.setAlignment(QtCore.Qt.AlignRight)
        layout_title = QtWidgets.QHBoxLayout()
        layout_title.addWidget(state_indicator)
        layout_title.addWidget(label_filename)
        layout_title.addStretch()

        if self.state == State.LYRICS_FOUND:
            label_lyrics.setStyleSheet(f"color: {Color_.light_green.value}")
        else:
            label_lyrics.setStyleSheet("")

        grid_layout_normal = QtWidgets.QGridLayout()
        grid_layout_normal.addLayout(layout_title, 0, 0, 1, 2)
        grid_layout_normal.addWidget(label_cover, 1, 0, 4, 1)
        grid_layout_normal.addWidget(label_title, 1, 1, 1, 1)
        grid_layout_normal.addWidget(label_artists, 2, 1, 1, 1)
        grid_layout_normal.addWidget(label_album, 3, 1, 1, 1)
        grid_layout_normal.addWidget(label_duration, 4, 1, 1, 1)
        grid_layout_normal.addWidget(label_lyrics, 0, 2, 5, 1)

        widget = QtWidgets.QWidget()
        widget.setLayout(grid_layout_normal)
        return widget

    def build_compact_ui(self, track: Track) -> QtWidgets.QWidget:
        """Sets up the layout as compact mode.

        Args:
            track (Track): Track containing the information to display.
        """
        state_indicator = StateIndicator(self.state, x=4)
        state_indicator.setToolTip(self.state.value)
        label_cover = QtWidgets.QLabel()
        label_cover.setPixmap(self.covers[Mode.COMPACT])
        label_cover.setFixedWidth(COVER_SIZE[Mode.COMPACT])
        label_title = QtWidgets.QLabel(track.get_title())
        label_title.setToolTip(f"{track.filename}\n{track.get_title()}")
        label_title.setStyleSheet(
            "QLabel { font-size: 15pt; font-weight: 800; } " + STYLESHEET_QTOOLTIP
        )
        label_artists = QtWidgets.QLabel(track.get_artists())
        label_artists.setToolTip(track.get_artists())
        label_artists.setStyleSheet(
            "QLabel { font-size: 12pt; font-weight: 600; } " + STYLESHEET_QTOOLTIP
        )
        label_lyrics = QtWidgets.QLabel(
            track.get_lyrics(lines=LYRICS_LINES[Mode.COMPACT])
        )
        label_lyrics.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )
        label_lyrics.setToolTip(track.get_lyrics())
        label_lyrics.setAlignment(QtCore.Qt.AlignRight)
        layout_title = QtWidgets.QHBoxLayout()
        layout_title.addWidget(state_indicator)
        layout_title.addWidget(label_title)
        layout_title.addStretch()

        if self.state == State.LYRICS_FOUND:
            label_lyrics.setStyleSheet(f"color: {Color_.light_green.value}")
        else:
            label_lyrics.setStyleSheet("")

        grid_layout_compact = QtWidgets.QGridLayout()
        grid_layout_compact.addWidget(label_cover, 0, 0, 2, 1)
        grid_layout_compact.addLayout(layout_title, 0, 1, 1, 1)
        grid_layout_compact.addWidget(label_artists, 1, 1, 1, 1)
        grid_layout_compact.addWidget(label_lyrics, 0, 2, 2, 1)

        widget = QtWidgets.QWidget()
        widget.setLayout(grid_layout_compact)
        return widget

    def switch_layout(self) -> None:
        if self.gtagger.mode == Mode.NORMAL:
            self.stacked_widget.setCurrentIndex(0)
        elif self.gtagger.mode == Mode.COMPACT:
            self.stacked_widget.setCurrentIndex(1)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Intercepts the mouse release event on the `QFrame`.

        Enables the user to (de)select a track layout by clicking on it.

        Args:
            event (QtGui.QMouseEvent): Mouse release event.
        """
        # Only take into account the left mouse button
        if event.button() != QtCore.Qt.LeftButton:
            return

        self.toggle_selection()

    def toggle_selection(self, force: Optional[bool] = None) -> None:
        """Toggles the selection of the track layout.

        Args:
            force (bool, optional): Force the selection or deselection of the tracks.
            Has not effect if it is not set. Defaults to None.
        """
        if force is not None:
            self.selected = force
        else:
            self.selected = not self.selected

        if self.selected:
            stylesheet = f"background-color: {Color_.dark_blue.value};"
        else:
            stylesheet = ""
        self.frame.setStyleSheet(stylesheet)

        if force is None:
            # Trigger the signal only on a mouse click event, not on key press events
            self.signal_mouse_event.emit()
