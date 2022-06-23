"""Application GUI.

Handles the creation of the GUI and the interactions with the user.
"""

import sys
import pathlib
from threading import Thread
import qtawesome
from PySide6 import QtCore, QtWidgets, QtGui

from tools import Tools, Track, TrackSearch, LyricsSearch


class MainWindow(QtWidgets.QWidget):
    """
    Main window of the GUI
    
    Attributes:
        tracks (list[Track]): Tracks added by the user to the table.
    """

    def __init__(self):
        super().__init__()

        self.tracks: list[Track] = []

        self.setup_ui()

    def setup_ui(self):
        self.icon_add_files = qtawesome.icon("ri.file-add-line", color="darkgreen")
        self.action_add_files = QtGui.QAction("Add files")
        self.action_add_files.setIcon(self.icon_add_files)

        self.icon_add_folder = qtawesome.icon("ri.folder-add-line", color="darkgreen")
        self.action_add_folder = QtGui.QAction("Add a folder")
        self.action_add_folder.setIcon(self.icon_add_folder)

        self.icon_read_tags = qtawesome.icon("ri.search-2-line", color="darkblue")
        self.action_search_lyrics = QtGui.QAction("Read the tags")
        self.action_search_lyrics.setIcon(self.icon_read_tags)
        self.action_search_lyrics.setEnabled(False)

        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_bar.setSizePolicy(QtWidgets.QSizePolicy())
        self.menu_bar.addAction(self.action_add_files)
        self.menu_bar.addAction(self.action_add_folder)
        self.menu_bar.addSeparator()
        self.menu_bar.addAction(self.action_search_lyrics)

        self.input_token = QtWidgets.QLineEdit()
        self.input_token.setPlaceholderText("Enter your Genius client access token")
        self.input_token.setToolTip("Enter token")
        self.input_token.setStyleSheet("border: 0px")
        regex_epx = QtCore.QRegularExpression("[a-zA-Z0-9_-]{64}")
        self.validator = QtGui.QRegularExpressionValidator(regex_epx, self)
        self.input_token.setValidator(self.validator)

        self.table_model = QtGui.QStandardItemModel()
        self.table_model.setColumnCount(4)
        self.table_model.setHorizontalHeaderLabels(
            ["File", "Title", "Artist", "Lyrics"]
        )
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.table_model)
        self.table.setSortingEnabled(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setMenuBar(self.menu_bar)
        self.layout.addWidget(self.input_token)
        self.layout.addWidget(self.table)

        self.action_add_files.triggered.connect(lambda: self.add_files(False))
        self.action_add_folder.triggered.connect(lambda: self.add_files(True))
        self.action_search_lyrics.triggered.connect(self.search_lyrics)
        self.input_token.textChanged.connect(self.token_changed)

    def select_directories(self) -> str:
        """Asks user to select a directory.

        Returns:
            str: Path of the directory.
        """
        directory_dialog = QtWidgets.QFileDialog()
        directory = directory_dialog.getExistingDirectory(caption="Select folder")
        if directory == "":
            return None
        return directory

    def select_files(self) -> list[str]:
        """Asks user to select one or multiple MP3 files.

        Returns:
            list[str]: Paths of the files.
        """
        file_dialog = QtWidgets.QFileDialog()
        files = file_dialog.getOpenFileNames(
            caption="Select files", filter="MP3 files (*.mp3)"
        )
        if len(files[0]) == 0:
            return None
        return files[0]

    def is_token_valid(self) -> bool:
        """Checks to see if the token is in a valid format.
        
        Genius client access token have a length of 64 characters,
        and may include letters, digits, '_' and '-'.

        Returns:
            bool: `True` if the token is valid.
        """
        validator_state = self.validator.validate(self.input_token.text(), 0)[0]
        return validator_state == QtGui.QValidator.State.Acceptable

    @QtCore.Slot()
    def add_files(self, select_directory: bool) -> None:
        """Adds the selected files to the table.

        Args:
            select_directory (bool): `True` if the user selected a directory.
        """
        if select_directory:
            directory = self.select_directories()
            if directory is None:
                return
            files = pathlib.Path(directory).rglob("*.mp3")
        else:
            files = self.select_files()
            if files is None:
                return

        self.thread_add_rows = Thread(target=self.run_add_files, args=(files,))
        self.thread_add_rows.start()

    def run_add_files(self, files: list[str]):
        """Runs the thread for `add_files()`.

        Args:
            files (list[str]): List of files to add to the table.
        """
        for file in files:
            track = Track(file)
            self.tracks.append(track)

            self.table_model.insertRow(self.table_model.rowCount())
            self.table_model.setItem(
                self.table_model.rowCount() - 1, 0, QtGui.QStandardItem(track.filename)
            )
            self.table_model.setItem(
                self.table_model.rowCount() - 1, 1, QtGui.QStandardItem(track.title)
            )
            self.table_model.setItem(
                self.table_model.rowCount() - 1,
                2,
                QtGui.QStandardItem(track.main_artist),
            )

    @QtCore.Slot()
    def search_lyrics(self) -> None:
        """Searches for the lyrics of the files in the table.
        """
        self.thread_search_lyrics = Thread(target=self.run_search_lyrics)
        self.thread_search_lyrics.start()

    def run_search_lyrics(self) -> None:
        """Runs the thread for `search_lyrics()`.
        """
        # todo display error
        if self.table_model.rowCount() == 0 or self.thread_add_rows.is_alive():
            return

        token = self.input_token.text()
        for row, track in enumerate(self.tracks):
            track_search = TrackSearch(token)
            track_search.search_track(track)
            lyrics_search = LyricsSearch(token)
            lyrics_search.search_lyrics(track)
            # todo multiline ?
            self.table_model.setItem(
                row,
                3,
                QtGui.QStandardItem(track.get_lyrics(150)),
            )

    @QtCore.Slot()
    def token_changed(self) -> None:
        """The token was changed by the user.
        """
        if len(self.input_token.text()) == 0:
            self.input_token.setStyleSheet("border: 0px")
            self.input_token.setToolTip("Enter token")
            self.action_search_lyrics.setEnabled(False)
        elif self.is_token_valid():
            self.input_token.setStyleSheet(
                f"border: 0px; background-color: {Tools.COLORS['lightgreen']}"
            )
            self.input_token.setToolTip("Valid token")
            self.action_search_lyrics.setEnabled(True)
        else:
            self.input_token.setStyleSheet(
                f"border: 0px; background-color: {Tools.COLORS['lightred']}"
            )
            self.input_token.setToolTip("Invalid token")
            self.action_search_lyrics.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
