"""Lyrics popup."""

from PySide6 import QtCore, QtWidgets


class PopupLyrics(QtWidgets.QDialog):
    """Popup to show the full lyrics of a track."""

    def __init__(self, parent):
        """Init PopupLyrics.

        Args:
            parent: Parent window.
        """
        super().__init__(parent)

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the UI of the window."""
        self.label_lyrics = QtWidgets.QLabel()

        self.layout_lyrics = QtWidgets.QVBoxLayout()
        self.layout_lyrics.addWidget(self.label_lyrics)

        self.widget_lyrics = QtWidgets.QWidget()
        self.widget_lyrics.setLayout(self.layout_lyrics)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.widget_lyrics)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.addWidget(self.scroll_area, 0, 0, 1, 1)

        self.setLayout(self.layout_)
        self.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)

    def set_lyrics(self, lyrics: str, title: str):
        """Set the `lyrics` to be shown.

        Args:
            lyrics (str): Lyrics to show.
            title (str): Title of the track.
        """
        self.label_lyrics.setText(lyrics)
        self.setWindowTitle(f"Lyrics for {title}")
