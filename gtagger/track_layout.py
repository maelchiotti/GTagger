"""Layout containing the informations of a track."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6 import QtCore, QtGui, QtWidgets

from gtagger.utils import COVER_SIZE, LYRICS_LINES, Color_, Mode, State

if TYPE_CHECKING:
    from main import GTagger

    from gtagger.track import Track


class TrackLayout(QtWidgets.QWidget):
    """Customized implementation of a `QWidget` containing the informations of a track.

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
        self.label_cover.setPixmap(self.covers[self.gtagger.mode])
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
        self.label_lyrics.setWordWrap(True)

        self.layout_title = QtWidgets.QHBoxLayout()
        self.layout_title.addWidget(self.state_indicator)
        self.layout_title.addWidget(self.label_filename)
        self.layout_title.addStretch()

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addLayout(self.layout_title, 0, 0, 1, 2)
        self.grid_layout.addWidget(self.label_cover, 1, 0, 4, 1)
        self.grid_layout.addWidget(self.label_title, 1, 1, 1, 1)
        self.grid_layout.addWidget(self.label_artists, 2, 1, 1, 1)
        self.grid_layout.addWidget(self.label_album, 3, 1, 1, 1)
        self.grid_layout.addWidget(self.label_duration, 4, 1, 1, 1)
        self.grid_layout.addWidget(self.label_lyrics, 0, 2, 5, 1)

        self.frame = QtWidgets.QFrame()
        self.frame.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        self.frame.setLayout(self.grid_layout)
        self.frame.mouseReleaseEvent = self.mouseReleaseEvent
        self.frame.resizeEvent = self.resizeFrame

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.frame, 0, 0, 1, 1)

        self.setLayout(self.layout_)

    def setup_compact_mode(self, track: Track):
        """Sets up the layout as compact mode.

        Args:
            track (Track): Track containing the informations to display.
        """
        self.state_indicator = StateIndicator(self.state, x=4)
        self.state_indicator.setToolTip(self.state.value)
        self.label_cover = QtWidgets.QLabel()
        self.label_cover.setPixmap(self.covers[self.gtagger.mode])
        self.label_cover.setFixedWidth(COVER_SIZE[self.gtagger.mode])
        self.label_title = QtWidgets.QLabel(track.get_title())
        self.label_title.setToolTip(track.filename)
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
        self.label_lyrics.setWordWrap(True)

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
        self.frame.resizeEvent = self.resizeFrame

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.addWidget(self.frame, 0, 0, 1, 1)

        self.setLayout(self.layout_)

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
            stylesheet = f"background-color: {Color_.dark_blue.value};"
            self.label_cover.setPixmap(self.covers[self.gtagger.mode])
        else:
            stylesheet = ""
            self.label_cover.setPixmap(self.covers[self.gtagger.mode])
        self.frame.setStyleSheet(stylesheet)

        self.signal_mouse_event.emit()

    def resizeFrame(self, newSize: QtGui.QResizeEvent):
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
