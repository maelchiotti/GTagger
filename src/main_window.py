"""Application's main window.

Handles the creation of the main window and the interactions with the user.
"""

import os
import pathlib
import logging as log
import qtawesome
import qdarktheme
from PySide6 import QtCore, QtWidgets, QtGui

from src.settings import SettingsWindow
from src.threads import ThreadSearchLyrics
from src.track import Track
from src.tools import VERSION, PATH_ICONS, Color_, ColorDark, ColorLight, State, Theme, IconTheme


class MainWindow(QtWidgets.QWidget):
    """
    Main window of the GUI.

    Attributes:
        tracks (dict[str, Track]): Tracks added by the user to the table.
        token_url (QtCore.QUrl): URL to the Genius web page to get a client access token.
        settings_window (QtWidgets.QMainWindow): Settings window.
        settings (SettingsWindow): Settings.
        thread_search_lyrics: (QtCore.QThread): Thread to search for the lyrics.
    """
    def __init__(self):
        super().__init__()
        
        self.theme = Theme.DARK

        self.tracks: dict[str, Track] = {}
        self.track_layouts: dict[str, TrackLayout] = {}
        self.token_url: QtCore.QUrl = QtCore.QUrl("https://genius.com/api-clients")

        self.settings_window: QtWidgets.QMainWindow = QtWidgets.QMainWindow(self)
        self.settings: SettingsWindow = SettingsWindow(self.settings_window)

        self.thread_search_lyrics: QtCore.QThread = None

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        self.setWindowTitle(f"GTagger ({VERSION})")
        
        icon_add_files = CustomIcon(IconTheme.OUTLINE, "documents", Color_.green, self.theme)
        self.action_add_files = QtGui.QAction()
        self.action_add_files.setIcon(icon_add_files)
        self.action_add_files.setToolTip("Select files")

        icon_add_folder = CustomIcon(IconTheme.OUTLINE, "folder-open", Color_.green, self.theme)
        self.action_add_folder = QtGui.QAction()
        self.action_add_folder.setIcon(icon_add_folder)
        self.action_add_folder.setToolTip("Select a folder")

        icon_read_tags = CustomIcon(IconTheme.OUTLINE, "pricetags", Color_.blue, self.theme)
        self.action_search_lyrics = QtGui.QAction()
        self.action_search_lyrics.setIcon(icon_read_tags)
        self.action_search_lyrics.setToolTip("Search for the lyrics")
        self.action_search_lyrics.setEnabled(False)

        icon_save_lyrics = CustomIcon(IconTheme.OUTLINE, "save", Color_.green, self.theme)
        self.action_save_lyrics = QtGui.QAction()
        self.action_save_lyrics.setIcon(icon_save_lyrics)
        self.action_save_lyrics.setToolTip("Save the lyrics")
        self.action_save_lyrics.setEnabled(True)

        icon_cancel_rows = CustomIcon(IconTheme.OUTLINE, "arrow-undo", Color_.orange, self.theme)
        self.action_cancel_rows = QtGui.QAction()
        self.action_cancel_rows.setIcon(icon_cancel_rows)
        self.action_cancel_rows.setToolTip("Cancel the modifications\nof selected rows")
        self.action_cancel_rows.setEnabled(False)

        icon_remove_rows = CustomIcon(IconTheme.OUTLINE, "remove-circle", Color_.red, self.theme)
        self.action_remove_rows = QtGui.QAction()
        self.action_remove_rows.setIcon(icon_remove_rows)
        self.action_remove_rows.setToolTip("Remove selected rows")
        self.action_remove_rows.setEnabled(False)

        icon_settings = CustomIcon(IconTheme.OUTLINE, "settings", Color_.grey, self.theme)
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

        self.layout_files = QtWidgets.QVBoxLayout()

        self.widget_files = QtWidgets.QWidget()
        self.widget_files.setLayout(self.layout_files)
        
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.widget_files)
        self.scroll_area.setWidgetResizable(True)
        
        self.layout_main = QtWidgets.QGridLayout()
        self.layout_main.addWidget(self.input_token, 0, 0, 1, 1)
        self.layout_main.addWidget(self.button_token, 0, 1, 1, 1)
        self.layout_main.addWidget(self.scroll_area, 1, 0, 1, 2)
        self.layout_main.setContentsMargins(5, 5, 5, 0)
        
        self.status_bar = QtWidgets.QStatusBar()
        
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setMenuBar(self.tool_bar)
        self.layout.addLayout(self.layout_main, 0, 0, 1, 1)
        self.layout.addWidget(self.status_bar, 1, 0, 1, 1)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.action_add_files.triggered.connect(lambda: self.add_files(False))
        self.action_add_folder.triggered.connect(lambda: self.add_files(True))
        self.action_search_lyrics.triggered.connect(self.search_lyrics)
        self.action_save_lyrics.triggered.connect(self.save_lyrics)
        self.action_cancel_rows.triggered.connect(self.cancel_rows)
        self.action_remove_rows.triggered.connect(self.remove_rows)
        self.action_settings.triggered.connect(self.open_settings)
        self.input_token.textChanged.connect(self.token_changed)
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
    def change_theme(self, theme: Theme):
        if theme == Theme.LIGHT:
            QtWidgets.QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet("light", "rounded"))
        elif theme == Theme.DARK:
            QtWidgets.QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet("dark", "rounded"))
        self.theme = theme

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

        for file in files:
            track = Track(file)
            tags_read = track.read_tags()
            self.tracks[track.filename] = track

            if tags_read:
                title = track.get_title()
                artists = track.get_artists()
                lyrics = track.get_lyrics()
                state = State.TAGS_READ.value
            else:
                title = "-"
                artists = "-"
                lyrics = "-"
                state = State.TAGS_NOT_READ.value
            
            track_layout = TrackLayout(track.filepath, track.filename, title, artists, lyrics, state)
            self.track_layouts[track.filename] = track_layout
            self.layout_files.addLayout(track_layout)

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
                f"border: 0px; background-color: {ColorLight.green.value}"
            )
            self.input_token.setToolTip("Valid token")
            self.action_search_lyrics.setEnabled(True)
        else:
            self.input_token.setStyleSheet(
                f"border: 0px; background-color: {ColorLight.red.value}"
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
                    row, 4, QtGui.QStandardItem(State.LYRICS_SAVED.value)
                )
            else:
                self.table_model.setItem(
                    row, 4, QtGui.QStandardItem(State.LYRICS_NOT_SAVED.value)
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


class CustomIcon(QtGui.QIcon):
    def __init__(self, icon_theme: IconTheme, icon_name: str, icon_color: Color_, theme: Theme):
        super().__init__()
        
        if icon_theme == IconTheme.NORMAL:
            image_path = os.path.join(PATH_ICONS, IconTheme.NORMAL.value, icon_name)
        if icon_theme == IconTheme.OUTLINE:
            icon_name = icon_name + "-" + IconTheme.OUTLINE.value + ".svg"
            image_path = os.path.join(PATH_ICONS, IconTheme.OUTLINE.value, icon_name)
        elif icon_theme == IconTheme.SHARP:
            icon_name = icon_name + "-" + IconTheme.SHARP.value + ".svg"
            image_path = os.path.join(PATH_ICONS, IconTheme.SHARP.value, icon_name)
        if not os.path.exists(image_path):
            log.error("The icon '%s' does not exist", icon_name)
            return
        image = QtGui.QPixmap(image_path)
        
        if theme == Theme.DARK:
            color = ColorLight.get_color(icon_color.value)
        elif theme == Theme.LIGHT:
            color = ColorDark.get_color(icon_color.value)
        
        painter = QtGui.QPainter(image)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceIn)
        painter.setBrush(QtGui.QColor(color.value))
        painter.setPen(QtGui.QColor(color.value))
        painter.drawRect(image.rect())
        painter.end()
        
        self.addPixmap(image)

        
class TrackLayout(QtWidgets.QGridLayout):
    def __init__(self, filepath: str, filename: str, title: str, artists: str, lyrics: str, state: str):
        super().__init__()
        
        self.label_filename = QtWidgets.QLabel(filename)
        self.label_filename.setToolTip(filepath)
        self.addWidget(self.label_filename, 0, 0, 1, 2)
        self.label_title = QtWidgets.QLabel(title)
        self.addWidget(self.label_title, 1, 0, 1, 1)
        self.label_artist = QtWidgets.QLabel(artists)
        self.addWidget(self.label_artist, 1, 1, 1, 1)
        self.label_lyrics = QtWidgets.QLabel(lyrics)
        self.addWidget(self.label_lyrics, 2, 0, 1, 2)
        self.label_state = QtWidgets.QLabel(state)
        self.addWidget(self.label_state, 3, 0, 1, 2)
