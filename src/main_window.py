"""Application's main window.

Handles the creation of the main window and the interactions with the user.
"""

import pathlib
import qtawesome
from PySide6 import QtCore, QtWidgets, QtGui

from src.settings import SettingsWindow
from src.threads import ThreadAddRows, ThreadSearchLyrics
from src.tools import Track, Colors, States

VERSION = "v1.0.0"


class MainWindow(QtWidgets.QWidget):
    """
    Main window of the GUI.

    Attributes:
        tracks (dict[str, Track]): Tracks added by the user to the table.
        token_url (QtCore.QUrl): URL to the Genius web page to get a client access token.
        settings_window (QtWidgets.QMainWindow): Settings window.
        settings (SettingsWindow): Settings.
        thread_add_rows: (QtCore.QThread): Thread to add rows to the table.
        thread_search_lyrics: (QtCore.QThread): Thread to search for the lyrics.
    """

    def __init__(self):
        super().__init__()

        self.tracks: dict[str, Track] = {}
        self.token_url: QtCore.QUrl = QtCore.QUrl("https://genius.com/api-clients")

        self.settings_window: QtWidgets.QMainWindow = QtWidgets.QMainWindow(self)
        self.settings: SettingsWindow = SettingsWindow(self.settings_window)

        self.thread_add_rows: QtCore.QThread = None
        self.thread_search_lyrics: QtCore.QThread = None

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        icon_add_files = qtawesome.icon("ri.file-add-line", color="darkgreen")
        self.action_add_files = QtGui.QAction()
        self.action_add_files.setIcon(icon_add_files)
        self.action_add_files.setToolTip("Select files")

        icon_add_folder = qtawesome.icon("ri.folder-add-line", color="darkgreen")
        self.action_add_folder = QtGui.QAction()
        self.action_add_folder.setIcon(icon_add_folder)
        self.action_add_folder.setToolTip("Select a folder")

        icon_read_tags = qtawesome.icon("ri.search-2-line", color="darkblue")
        self.action_search_lyrics = QtGui.QAction()
        self.action_search_lyrics.setIcon(icon_read_tags)
        self.action_search_lyrics.setToolTip("Search for the lyrics")
        self.action_search_lyrics.setEnabled(False)

        icon_save_lyrics = qtawesome.icon("ri.save-3-line", color="darkgreen")
        self.action_save_lyrics = QtGui.QAction()
        self.action_save_lyrics.setIcon(icon_save_lyrics)
        self.action_save_lyrics.setToolTip("Save the lyrics")
        self.action_save_lyrics.setEnabled(True)

        icon_cancel_rows = qtawesome.icon("ri.arrow-go-back-fill", color="darkorange")
        self.action_cancel_rows = QtGui.QAction()
        self.action_cancel_rows.setIcon(icon_cancel_rows)
        self.action_cancel_rows.setToolTip("Cancel the modifications\nof selected rows")
        self.action_cancel_rows.setEnabled(False)

        icon_remove_rows = qtawesome.icon("ri.delete-row", color="darkred")
        self.action_remove_rows = QtGui.QAction()
        self.action_remove_rows.setIcon(icon_remove_rows)
        self.action_remove_rows.setToolTip("Remove selected rows")
        self.action_remove_rows.setEnabled(False)

        icon_settings = qtawesome.icon("ri.settings-3-line")
        self.action_settings = QtGui.QAction()
        self.action_settings.setIcon(icon_settings)
        self.action_settings.setToolTip("Settings")

        self.tool_bar = QtWidgets.QToolBar()
        self.tool_bar.setIconSize(QtCore.QSize(30, 30))
        self.tool_bar.addAction(self.action_add_files)
        self.tool_bar.addAction(self.action_add_folder)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.action_search_lyrics)
        self.tool_bar.addAction(self.action_save_lyrics)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.action_cancel_rows)
        self.tool_bar.addAction(self.action_remove_rows)
        self.tool_bar.addSeparator()
        self.tool_bar.addAction(self.action_settings)

        self.input_token = QtWidgets.QLineEdit()
        self.input_token.setPlaceholderText("Enter your Genius client access token")
        self.input_token.setToolTip("Enter token")
        self.input_token.setStyleSheet("border: 0px")
        regex_epx = QtCore.QRegularExpression("[a-zA-Z0-9_-]{64}")
        self.validator = QtGui.QRegularExpressionValidator(regex_epx, self)
        self.input_token.setValidator(self.validator)

        self.icon_token = qtawesome.icon("ri.external-link-fill")
        self.button_token = QtWidgets.QPushButton()
        self.button_token.setIcon(self.icon_token)
        self.button_token.setToolTip("Get the token\non Genius website")

        self.table_model = QtGui.QStandardItemModel()
        self.table_model.setColumnCount(4)
        self.table_model.setHorizontalHeaderLabels(
            ["File", "Title", "Artist", "Lyrics", "State"]
        )
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.table_model)
        self.table.setSortingEnabled(True)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setMenuBar(self.tool_bar)
        self.layout.addWidget(self.input_token, 0, 0, 1, 1)
        self.layout.addWidget(self.button_token, 0, 1, 1, 1)
        self.layout.addWidget(self.table, 1, 0, 1, 2)

        self.setWindowTitle(f"GTagger ({VERSION})")

        self.action_add_files.triggered.connect(lambda: self.add_files(False))
        self.action_add_folder.triggered.connect(lambda: self.add_files(True))
        self.action_search_lyrics.triggered.connect(self.search_lyrics)
        self.action_save_lyrics.triggered.connect(self.save_lyrics)
        self.action_cancel_rows.triggered.connect(self.cancel_rows)
        self.action_remove_rows.triggered.connect(self.remove_rows)
        self.action_settings.triggered.connect(self.open_settings)
        self.input_token.textChanged.connect(self.token_changed)
        self.table_model.itemChanged.connect(self.table_changed)
        self.button_token.clicked.connect(self.open_token_page)

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
            if self.settings.get_setting("recursive"):
                files = pathlib.Path(directory).rglob("*.mp3")
            else:
                files = pathlib.Path(directory).glob("*.mp3")
        else:
            files = self.select_files()
            if files is None:
                return

        self.thread_add_rows = ThreadAddRows(self, files)
        self.thread_add_rows.start()

    @QtCore.Slot()
    def search_lyrics(self) -> None:
        """Searches for the lyrics of the files and adds them in the table."""
        self.thread_search_lyrics = ThreadSearchLyrics(self)
        self.thread_search_lyrics.start()

    @QtCore.Slot()
    def token_changed(self) -> None:
        """The token was changed by the user."""
        if len(self.input_token.text()) == 0:
            self.input_token.setStyleSheet("border: 0px")
            self.input_token.setToolTip("Enter token")
            self.action_search_lyrics.setEnabled(False)
        elif self.is_token_valid():
            self.input_token.setStyleSheet(
                f"border: 0px; background-color: {Colors.lightgreen.value}"
            )
            self.input_token.setToolTip("Valid token")
            self.action_search_lyrics.setEnabled(True)
        else:
            self.input_token.setStyleSheet(
                f"border: 0px; background-color: {Colors.lightred.value}"
            )
            self.input_token.setToolTip("Invalid token")
            self.action_search_lyrics.setEnabled(False)

    @QtCore.Slot()
    def table_changed(self) -> None:
        """The model of the table has changed."""
        if self.table_model.rowCount() > 0:
            self.action_cancel_rows.setEnabled(True)
            self.action_remove_rows.setEnabled(True)
        else:
            self.action_cancel_rows.setEnabled(False)
            self.action_remove_rows.setEnabled(False)

    @QtCore.Slot()
    def save_lyrics(self) -> None:
        """Saves the lyrics to the files."""
        for row in range(self.table_model.rowCount()):
            filename = self.table_model.item(row, 0).text()
            track = self.tracks[filename]
            saved = track.save_lyrics()
            if saved:
                self.table_model.setItem(
                    row, 4, QtGui.QStandardItem(States.LYRICS_SAVED.value)
                )
            else:
                self.table_model.setItem(
                    row, 4, QtGui.QStandardItem(States.LYRICS_NOT_SAVED.value)
                )

    @QtCore.Slot()
    def cancel_rows(self) -> None:
        """Removes the added lyrics from the files."""
        selection = self.table.selectedIndexes()
        for item in selection:
            filename = self.table_model.item(item.row(), 0).text()
            track = self.tracks[filename]
            track.lyrics = None
            self.table_model.item(item.row(), 3).setText("")

    @QtCore.Slot()
    def remove_rows(self) -> None:
        """Remove the selected rows."""
        selection = sorted(self.table.selectedIndexes(), reverse=True)
        prev_index = -1
        for item in selection:
            index = item.row()
            if index != prev_index:
                filename = self.table_model.item(index, 0).text()
                self.tracks.pop(filename)
                self.table_model.removeRow(index)
            prev_index = index

    @QtCore.Slot()
    def open_token_page(self) -> None:
        """Opens the Genius website to fetch the client access token."""
        QtGui.QDesktopServices.openUrl(self.token_url)

    @QtCore.Slot()
    def open_settings(self) -> None:
        """Opens the settings window."""
        self.settings_window.show()
