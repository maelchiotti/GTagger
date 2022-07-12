"""Application's main window.

Handles the creation of the main window and the interactions with the user.
"""

import pathlib
import qdarktheme
from PySide6 import QtCore, QtWidgets, QtGui

from src.settings import SettingsWindow
from src.track import Track
from src.lyrics_search import ThreadLyricsSearch
from src.tools import (
    VERSION,
    CustomIcon,
    TrackLayout,
    Color_,
    ColorLight,
    State,
    Theme,
    IconTheme,
)


class MainWindow(QtWidgets.QWidget):
    """
    Main window of the GUI.

    Attributes:
        gtagger (QtWidgets.QApplication): Current instance of the application. Mainly used to retrieve its theme anywhere.
        tracks (dict[str, Track]): Tracks added by the user.
        track_layouts (dict[Track, TrackLayout]): Layouts containing the informations of the tracks added by the user.
        token_url (QtCore.QUrl): URL to the Genius web page to get a client access token.
        settings_window (QtWidgets.QMainWindow): Settings window.
        settings (SettingsWindow): Settings.
        thread_search_lyrics: (QtCore.QThread): Thread to search for the lyrics.
    """

    def __init__(self):
        super().__init__()
        self.gtagger = QtWidgets.QApplication.instance()

        self.tracks: dict[str, Track] = {}
        self.track_layouts: dict[Track, TrackLayout] = {}
        self.token_url: QtCore.QUrl = QtCore.QUrl("https://genius.com/api-clients")

        self.settings_window: QtWidgets.QMainWindow = QtWidgets.QMainWindow(self)
        self.settings: SettingsWindow = SettingsWindow(self.settings_window)

        self.thread_search_lyrics: QtCore.QThread = None

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        self.setWindowTitle(f"GTagger ({VERSION})")

        self.action_add_files = QtGui.QAction()
        self.action_add_files.setToolTip("Select files")

        self.action_add_folder = QtGui.QAction()
        self.action_add_folder.setToolTip("Select a folder")

        self.action_search_lyrics = QtGui.QAction()
        self.action_search_lyrics.setToolTip("Search for the lyrics")
        self.action_search_lyrics.setEnabled(False)

        self.action_save_lyrics = QtGui.QAction()
        self.action_save_lyrics.setToolTip("Save the lyrics")
        self.action_save_lyrics.setEnabled(False)

        self.action_cancel_rows = QtGui.QAction()
        self.action_cancel_rows.setToolTip("Cancel the modifications\nof selected rows")
        self.action_cancel_rows.setEnabled(False)

        self.action_remove_rows = QtGui.QAction()
        self.action_remove_rows.setToolTip("Remove selected rows")
        self.action_remove_rows.setEnabled(False)

        self.action_settings = QtGui.QAction()
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

        self.button_token = QtWidgets.QPushButton()
        self.button_token.setToolTip("Get the token\non Genius website")

        self.layout_files = QtWidgets.QVBoxLayout()
        self.layout_files.setAlignment(QtCore.Qt.AlignTop)

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

        self.button_theme = QtWidgets.QPushButton()
        self.button_theme.setToolTip("Change to light theme")

        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.addPermanentWidget(self.button_theme)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setMenuBar(self.tool_bar)
        self.layout.addLayout(self.layout_main, 0, 0, 1, 1)
        self.layout.addWidget(self.status_bar, 1, 0, 1, 1)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setup_icons()

        self.action_add_files.triggered.connect(lambda: self.add_files(False))
        self.action_add_folder.triggered.connect(lambda: self.add_files(True))
        self.action_search_lyrics.triggered.connect(self.search_lyrics)
        self.action_save_lyrics.triggered.connect(self.save_lyrics)
        self.action_cancel_rows.triggered.connect(self.cancel_rows)
        self.action_remove_rows.triggered.connect(self.remove_rows)
        self.action_settings.triggered.connect(self.open_settings)
        self.input_token.textChanged.connect(self.token_changed)
        self.button_token.clicked.connect(self.open_token_page)
        self.button_theme.clicked.connect(self.change_theme)

    def setup_icons(self):
        """Sets up the icons for all the buttons of the application and the covers placeholders."""
        theme = self.gtagger.theme

        # Change the icons
        icon_add_files = CustomIcon(IconTheme.OUTLINE, "documents", Color_.green, theme)
        icon_add_folder = CustomIcon(
            IconTheme.OUTLINE, "folder-open", Color_.green, theme
        )
        icon_search_lyrics = CustomIcon(IconTheme.OUTLINE, "search", Color_.blue, theme)
        icon_save_lyrics = CustomIcon(IconTheme.OUTLINE, "save", Color_.green, theme)
        icon_cancel_rows = CustomIcon(
            IconTheme.OUTLINE, "arrow-undo", Color_.orange, theme
        )
        icon_remove_rows = CustomIcon(
            IconTheme.OUTLINE, "remove-circle", Color_.red, theme
        )
        icon_settings = CustomIcon(IconTheme.OUTLINE, "settings", Color_.grey, theme)
        icon_token = CustomIcon(IconTheme.OUTLINE, "open", Color_.grey, theme)
        if theme == Theme.DARK:
            icon_theme = CustomIcon(IconTheme.OUTLINE, "sunny", Color_.grey, theme)
        elif theme == Theme.LIGHT:
            icon_theme = CustomIcon(IconTheme.OUTLINE, "moon", Color_.grey, theme)

        self.action_add_files.setIcon(icon_add_files)
        self.action_add_folder.setIcon(icon_add_folder)
        self.action_search_lyrics.setIcon(icon_search_lyrics)
        self.action_save_lyrics.setIcon(icon_save_lyrics)
        self.action_cancel_rows.setIcon(icon_cancel_rows)
        self.action_remove_rows.setIcon(icon_remove_rows)
        self.action_settings.setIcon(icon_settings)
        self.button_token.setIcon(icon_token)
        self.button_theme.setIcon(icon_theme)

        # Change the cover placeholders if needed
        for track in self.tracks.values():
            track_layout = self.track_layouts[track]
            if not track_layout.selected:
                track_layout.label_cover.setPixmap(track.covers[theme])

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

        Genius client access token have a length of 64 characters, and may include letters, digits, '_' and '-'.

        Returns:
            bool: `True` if the token is valid.
        """
        validator_state = self.validator.validate(self.input_token.text(), 0)[0]
        return validator_state == QtGui.QValidator.State.Acceptable

    @QtCore.Slot()
    def change_theme(self):
        """Changes the theme of the application."""
        if self.gtagger.theme == Theme.LIGHT:
            self.gtagger.theme = Theme.DARK
            self.button_theme.setToolTip("Change to light theme")
            self.gtagger.setStyleSheet(qdarktheme.load_stylesheet("dark", "rounded"))
        elif self.gtagger.theme == Theme.DARK:
            self.gtagger.theme = Theme.LIGHT
            self.button_theme.setToolTip("Change to dark theme")
            self.gtagger.setStyleSheet(qdarktheme.load_stylesheet("light", "rounded"))
        self.setup_icons()

    @QtCore.Slot()
    def add_files(self, select_directory: bool) -> None:
        """Adds the selected files to the table.

        Args:
            select_directory (bool): `True` if the user selected a directory.
        """
        # Construct the list of files
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

        # Add the layouts with files' informations
        for file in files:
            track = Track(file)
            tags_read = track.read_tags()

            # Skip the file if the tags could not be read
            if not tags_read:
                continue

            self.tracks[track.filename] = track
            track_layout = TrackLayout(
                track.get_filepath(),
                track.filename,
                track.covers,
                track.get_duration(),
                track.get_title(),
                track.get_artists(),
                track.get_lyrics(lines=5),
                State.TAGS_READ.value,
                self.gtagger.theme,
            )
            track_layout.signal_mouse_event.connect(self.toggle_actions_cancel_remove)
            self.track_layouts[track] = track_layout
            self.layout_files.addLayout(track_layout)

    @QtCore.Slot()
    def search_lyrics(self) -> None:
        """Searches for the lyrics of the files and adds them in the table."""
        token = self.input_token.text()
        self.thread_search_lyrics = ThreadLyricsSearch(token, self.track_layouts)
        self.thread_search_lyrics.start()

    @QtCore.Slot()
    def token_changed(self) -> None:
        """The token was changed by the user."""
        if len(self.input_token.text()) == 0:
            # Input is empty
            self.input_token.setStyleSheet("border: 0px")
            self.input_token.setToolTip("Enter token")
            self.action_search_lyrics.setEnabled(False)
        elif self.is_token_valid():
            # Token is valid
            self.input_token.setStyleSheet(
                f"border: 0px; background-color: {ColorLight.green.value}"
            )
            self.input_token.setToolTip("Valid token")
            self.action_search_lyrics.setEnabled(True)
        else:
            # Token is not valid
            self.input_token.setStyleSheet(
                f"border: 0px; background-color: {ColorLight.red.value}"
            )
            self.input_token.setToolTip("Invalid token")
            self.action_search_lyrics.setEnabled(False)

    @QtCore.Slot()
    def save_lyrics(self) -> None:
        """Saves the lyrics to the files."""
        for track, track_layout in self.track_layouts.items():
            saved = track.save_lyrics()
            if saved:
                track_layout.label_state.setText(State.LYRICS_SAVED.value)
            else:
                track_layout.label_state.setText(State.LYRICS_NOT_SAVED.value)

    @QtCore.Slot()
    def toggle_actions_cancel_remove(self) -> None:
        """Toggles the buttons for cancelling the lyrics and removing tracks."""
        for track_layout in self.track_layouts.values():
            if track_layout.selected:
                self.action_cancel_rows.setEnabled(True)
                self.action_remove_rows.setEnabled(True)
                return
        self.action_cancel_rows.setEnabled(False)
        self.action_remove_rows.setEnabled(False)

    @QtCore.Slot()
    def cancel_rows(self) -> None:
        """Removes the added lyrics from the files."""
        for track, track_layout in self.track_layouts.items():
            if track_layout.selected:
                track.lyrics.set(track.eyed3_tags.lyrics)
                track_layout.label_lyrics.setText(track.get_lyrics(lines=5))

    @QtCore.Slot()
    def remove_rows(self) -> None:
        """Remove the selected rows."""
        for track, track_layout in self.track_layouts.copy().items():
            if track_layout.selected:
                track_layout.frame.hide()
                self.layout_files.removeItem(track_layout)
                self.track_layouts.pop(track)
        self.toggle_actions_cancel_remove()

    @QtCore.Slot()
    def open_token_page(self) -> None:
        """Opens the Genius website to fetch the client access token."""
        QtGui.QDesktopServices.openUrl(self.token_url)

    @QtCore.Slot()
    def open_settings(self) -> None:
        """Opens the settings window."""
        self.settings_window.show()
