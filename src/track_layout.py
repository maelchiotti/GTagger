"""Layout containing the information of a track."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from PySide6 import QtCore, QtGui, QtWidgets

from src.consts import (
    LINES_LYRICS,
    SIZE_COVER,
    SIZE_ICON_INDICATOR,
    STYLESHEET_QTOOLTIP,
)
from src.enums import CustomColors, State
from src.icons import get_icon
from src.track import Track

if TYPE_CHECKING:
    from gtagger import GTagger


class TrackLayout(QtWidgets.QFrame):
    """Custom implementation of a `QFrame` containing the information of a track.

    Signals:
        signal_mouse_event (QtCore.Signal): Emitted when a mouse event is intercepted.

    Attributes:
        track (Track): Track to display.
        state (State): State of the track.
        selected (bool): `True` if the track is currently selected.
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

        self.track = track
        self.state: State = state
        self.selected: bool = False
        self.gtagger: GTagger = gtagger

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the UI of the window."""
        self.label_filename = QtWidgets.QLabel(self.track.filename)
        self.label_filename.setToolTip(self.track.get_filepath())
        self.button_play = QtWidgets.QPushButton()
        self.button_play.setToolTip("Play the track in the default application")
        icon_color = self.state.value.value
        self.button_play.setIcon(
            get_icon("play-circle", color=icon_color, color_active=icon_color)
        )
        self.button_play.setStyleSheet(f"""icon-size: {SIZE_ICON_INDICATOR}px""")
        self.button_play.setFixedSize(SIZE_ICON_INDICATOR, SIZE_ICON_INDICATOR)
        self.button_play.setFlat(True)
        self.label_cover = QtWidgets.QLabel()
        self.label_cover.setPixmap(self.track.cover)
        self.label_cover.setFixedWidth(SIZE_COVER)
        self.label_title = QtWidgets.QLabel(self.track.get_title())
        self.label_title.setToolTip(self.track.get_title())
        self.label_title.setStyleSheet(
            "QLabel { font-size: 15pt; font-weight: 800; } " + STYLESHEET_QTOOLTIP
        )
        self.label_artists = QtWidgets.QLabel(self.track.get_artists())
        self.label_artists.setToolTip(self.track.get_artists())
        self.label_artists.setStyleSheet(
            "QLabel { font-size: 12pt; font-weight: 600; } " + STYLESHEET_QTOOLTIP
        )
        self.label_album = QtWidgets.QLabel(self.track.get_album())
        self.label_album.setToolTip(self.track.get_album())
        self.label_album.setStyleSheet(
            "QLabel { font-size: 11pt; font-weight: 400; } " + STYLESHEET_QTOOLTIP
        )
        self.label_duration = QtWidgets.QLabel(f"<i>{self.track.get_duration()}</i>")
        self.label_duration.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_lyrics = QtWidgets.QLabel(self.track.get_lyrics(lines=LINES_LYRICS))
        self.label_lyrics.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Preferred,
        )
        self.label_lyrics.setToolTip(self.track.get_lyrics())
        self.label_lyrics.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignCenter
        )

        self.layout_title = QtWidgets.QHBoxLayout()
        self.layout_title.addWidget(self.button_play)
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
        self.setFrameStyle(
            QtWidgets.QFrame.Shape.StyledPanel | QtWidgets.QFrame.Shadow.Plain
        )

        self.button_play.clicked.connect(self.play)
        self.mouseReleaseEvent = self.mouseReleaseEvent

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        """Intercept the mouse release event on the `QFrame`.

        Enables the user to (de)select a track layout by clicking on it.

        Args:
            event (QtGui.QMouseEvent): Mouse release event.
        """
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            # Only take into account the left mouse button
            return

        self.toggle_selection()

    def toggle_selection(self, force: Optional[bool] = None) -> None:
        """Toggle the selection of the track layout.

        Args:
            force (Optional[bool]): Force the selection or deselection of the tracks. Has no effect if it is not set. Defaults to None.
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

    def play(self) -> None:
        """Play the track in the default application."""
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(self.track.filepath))

    def set_state(self, state: State) -> None:
        """Set the state of the track.

        Args:
            state (State): State of the track.

        Change the color of the play button.
        """
        self.state = state
        icon_color = self.state.value.value
        self.button_play.setIcon(
            get_icon("play-circle", color=icon_color, color_active=icon_color)
        )
