"""Application's help window.

Handles the creation of the help window.
"""

from PySide6 import QtCore, QtWidgets

from src.consts import SIZE_ICON_INDICATOR
from src.enums import State
from src.icons import get_icon


class WindowHelp(QtWidgets.QDialog):
    """Help window of the GUI."""

    def __init__(self, parent):
        """Init WindowHelp.

        Args:
            parent: Parent window.
        """
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the UI of the window."""
        # Usage
        self.label_usage = QtWidgets.QLabel(
            """
            The usual workflow of GTagger is the following:<br/>
            - Add individual files or an entire folder (a recursive search can be enabled in the settings).<br/>
            - Add your Genius client access token.<br/>
            - Use the <i>Search</i> button to search for the lyrics.<br/>
            - Use the <i>Cancel</i> button to discard the added lyrics if they are wrong,
            or the <i>Remove</i> button to discard the file entirely.<br/>
            - Use the <i>Save</i> button to save the lyrics to the files.
            <br/><br/>
            Shortcuts:<br/>
            - Ctrl+A: Select all files.<br/>
            - Ctrl+D: Deselect all files.
            """
        )
        self.label_usage.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_usage.setWordWrap(True)

        self.layout_usage = QtWidgets.QGridLayout()
        self.layout_usage.addWidget(self.label_usage, 0, 0, 1, 1)

        self.frame_usage = QtWidgets.QFrame()
        self.frame_usage.setFrameStyle(
            QtWidgets.QFrame.Shape.StyledPanel | QtWidgets.QFrame.Shadow.Plain
        )
        self.frame_usage.setLayout(self.layout_usage)

        # State indicator icons
        icon_blue = get_icon("play-circle", color=State.TAGS_READ.value.value)
        icon_green = get_icon("play-circle", color=State.LYRICS_FOUND.value.value)
        icon_orange = get_icon("play-circle", color=State.LYRICS_NOT_FOUND.value.value)
        icon_yellow_genius = get_icon(
            "play-circle", color=State.LYRICS_SAVED.value.value
        )
        icon_red = get_icon("play-circle", color=State.LYRICS_NOT_SAVED.value.value)
        self.label_icon_blue = QtWidgets.QLabel()
        self.label_icon_blue.setPixmap(
            icon_blue.pixmap(SIZE_ICON_INDICATOR, SIZE_ICON_INDICATOR)
        )
        self.label_icon_blue.setFixedWidth(SIZE_ICON_INDICATOR)
        self.label_icon_green = QtWidgets.QLabel()
        self.label_icon_green.setPixmap(
            icon_green.pixmap(SIZE_ICON_INDICATOR, SIZE_ICON_INDICATOR)
        )
        self.label_icon_green.setFixedWidth(SIZE_ICON_INDICATOR)
        self.label_icon_orange = QtWidgets.QLabel()
        self.label_icon_orange.setPixmap(
            icon_orange.pixmap(SIZE_ICON_INDICATOR, SIZE_ICON_INDICATOR)
        )
        self.label_icon_orange.setFixedWidth(SIZE_ICON_INDICATOR)
        self.label_icon_yellow_genius = QtWidgets.QLabel()
        self.label_icon_yellow_genius.setPixmap(
            icon_yellow_genius.pixmap(SIZE_ICON_INDICATOR, SIZE_ICON_INDICATOR)
        )
        self.label_icon_yellow_genius.setFixedWidth(SIZE_ICON_INDICATOR)
        self.label_icon_red = QtWidgets.QLabel()
        self.label_icon_red.setPixmap(
            icon_red.pixmap(SIZE_ICON_INDICATOR, SIZE_ICON_INDICATOR)
        )
        self.label_icon_red.setFixedWidth(SIZE_ICON_INDICATOR)

        self.label_state_indicator_title = QtWidgets.QLabel(
            """
            The state indicator, that can be clicked to play the track in the default application,
            indicates the following states:
            """
        )
        self.label_state_indicator_title.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_state_indicator_title.setWordWrap(True)
        self.label_state_indicator_read = QtWidgets.QLabel(
            """
            The tags of the track were read successfully.
            """
        )
        self.label_state_indicator_read.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_state_indicator_found = QtWidgets.QLabel(
            """
            The lyrics of the track were found successfully.
            """
        )
        self.label_state_indicator_found.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_state_indicator_not_found = QtWidgets.QLabel(
            """
            The lyrics of the track were not found.
            """
        )
        self.label_state_indicator_not_found.setTextFormat(
            QtCore.Qt.TextFormat.RichText
        )
        self.label_state_indicator_saved = QtWidgets.QLabel(
            """
            The lyrics of the track were saved successfully.
            """
        )
        self.label_state_indicator_saved.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_state_indicator_not_saved = QtWidgets.QLabel(
            """
            The lyrics of the track were not saved.
            """
        )
        self.label_state_indicator_not_saved.setTextFormat(
            QtCore.Qt.TextFormat.RichText
        )

        self.layout_legend = QtWidgets.QGridLayout()

        self.layout_legend.addWidget(self.label_icon_blue, 0, 0, 1, 2)
        self.layout_legend.addWidget(self.label_icon_green, 1, 0, 1, 1)
        self.layout_legend.addWidget(self.label_icon_orange, 2, 0, 1, 1)
        self.layout_legend.addWidget(self.label_icon_yellow_genius, 3, 0, 1, 1)
        self.layout_legend.addWidget(self.label_icon_red, 4, 0, 1, 1)

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
            QtWidgets.QFrame.Shape.StyledPanel | QtWidgets.QFrame.Shadow.Plain
        )
        self.frame_state_indicator.setLayout(self.layout_state_indicator)

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.addWidget(self.frame_usage, 0, 0, 1, 1)
        self.layout_.addWidget(self.frame_state_indicator, 1, 0, 1, 1)

        self.setLayout(self.layout_)
        self.setWindowTitle("Help")
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
