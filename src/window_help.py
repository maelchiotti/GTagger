"""Application's informations window.

Handles the creation of the informations window.
"""

from PySide6 import QtCore, QtWidgets

from src.tools import State, StateIndicator

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.window_main import WindowMain


class WindowHelp(QtWidgets.QWidget):
    """Help window of the GUI.

    Args:
        gtagger (GTagger): GTagger application.
        window (QtWidgets.QMainWindow): Window UI.

    Attributes:
        gtagger (GTagger): GTagger application.
        window (QtWidgets.QMainWindow): Window UI.
    """

    def __init__(self, parent, ui_window: QtWidgets.QMainWindow):
        super().__init__(parent)

        self.main: WindowMain = parent
        self.window: QtWidgets.QMainWindow = ui_window

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        # Usage
        self.label_usage = QtWidgets.QLabel(
            """
            The usual workflow of GTagger is the following:
            <br/><br/>
            - Add individual files or an entire folder (a recursive search can be enabled in the settings).<br/>
            - Add your Genius client access token.<br/>
            - Use the <i>Search</i> button to search for the lyrics.<br/>
            - Use the <i>Cancel</i> button to discard the added lyrics if they are wrong, or the <i>Remove</i> button to discard the file entirely.<br/>
            - Use the <i>Save</i> button to save the lyrics to the files.
            """
        )
        self.label_usage.setTextFormat(QtCore.Qt.RichText)
        self.label_usage.setWordWrap(True)

        self.layout_usage = QtWidgets.QGridLayout()
        self.layout_usage.addWidget(self.label_usage, 0, 0, 1, 1)

        self.frame_usage = QtWidgets.QFrame()
        self.frame_usage.setFrameStyle(
            QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain
        )
        self.frame_usage.setLayout(self.layout_usage)

        # State indicator legend
        self.indicator_blue = StateIndicator(State.TAGS_READ, x=0, y=0, w=20, h=20)
        self.indicator_green = StateIndicator(State.LYRICS_FOUND, x=0, y=0, w=20, h=20)
        self.indicator_orange = StateIndicator(
            State.LYRICS_NOT_FOUND, x=0, y=0, w=20, h=20
        )
        self.indicator_yellow_genius = StateIndicator(
            State.LYRICS_SAVED, x=0, y=0, w=20, h=20
        )
        self.indicator_red = StateIndicator(
            State.LYRICS_NOT_SAVED, x=0, y=0, w=20, h=20
        )

        self.label_state_indicator_title = QtWidgets.QLabel(
            """
            The state indicator indicates the following states:
            <br/>
            """
        )
        self.label_state_indicator_title.setTextFormat(QtCore.Qt.RichText)
        self.label_state_indicator_title.setWordWrap(True)
        self.label_state_indicator_read = QtWidgets.QLabel(
            """
            The tags of the track were read successfully.
            """
        )
        self.label_state_indicator_read.setTextFormat(QtCore.Qt.RichText)
        self.label_state_indicator_found = QtWidgets.QLabel(
            """
            The lyrics of the track were found successfully.
            """
        )
        self.label_state_indicator_found.setTextFormat(QtCore.Qt.RichText)
        self.label_state_indicator_not_found = QtWidgets.QLabel(
            """
            The lyrics of the track were not found.
            """
        )
        self.label_state_indicator_not_found.setTextFormat(QtCore.Qt.RichText)
        self.label_state_indicator_saved = QtWidgets.QLabel(
            """
            The lyrics of the track were saved successfully.
            """
        )
        self.label_state_indicator_saved.setTextFormat(QtCore.Qt.RichText)
        self.label_state_indicator_not_saved = QtWidgets.QLabel(
            """
            The lyrics of the track were not saved.
            """
        )
        self.label_state_indicator_not_saved.setTextFormat(QtCore.Qt.RichText)

        self.layout_legend = QtWidgets.QGridLayout()

        self.layout_legend.addWidget(self.indicator_blue, 0, 0, 1, 2)
        self.layout_legend.addWidget(self.indicator_green, 1, 0, 1, 1)
        self.layout_legend.addWidget(self.indicator_orange, 2, 0, 1, 1)
        self.layout_legend.addWidget(self.indicator_yellow_genius, 3, 0, 1, 1)
        self.layout_legend.addWidget(self.indicator_red, 4, 0, 1, 1)

        self.layout_legend.addWidget(self.label_state_indicator_read, 0, 1, 1, 1)
        self.layout_legend.addWidget(self.label_state_indicator_found, 1, 1, 1, 1)
        self.layout_legend.addWidget(self.label_state_indicator_not_found, 2, 1, 1, 1)
        self.layout_legend.addWidget(self.label_state_indicator_saved, 3, 1, 1, 1)
        self.layout_legend.addWidget(self.label_state_indicator_not_saved, 4, 1, 1, 1)

        self.layout_state_indicator = QtWidgets.QGridLayout()
        self.layout_state_indicator.addWidget(
            self.label_state_indicator_title, 0, 0, 1, 1
        )
        self.layout_state_indicator.addLayout(self.layout_legend, 1, 0, 1, 1)

        self.frame_state_indicator = QtWidgets.QFrame()
        self.frame_state_indicator.setFrameStyle(
            QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain
        )
        self.frame_state_indicator.setLayout(self.layout_state_indicator)

        self.centralwidget = QtWidgets.QWidget(self.window)
        self.layout_ = QtWidgets.QGridLayout(self.centralwidget)
        self.layout_.addWidget(self.frame_usage, 0, 0, 1, 1)
        self.layout_.addWidget(self.frame_state_indicator, 1, 0, 1, 1)

        self.window.setCentralWidget(self.centralwidget)
        self.window.setWindowTitle("Help")