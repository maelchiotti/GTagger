"""Application's main window.

Handles the creation of the main window and the interactions with the user.
"""

from __future__ import annotations

from pathlib import Path
from PySide6 import QtCore, QtWidgets, QtGui
from src.window_help import WindowHelp
from src.window_informations import WindowInformations

from src.window_settings import WindowSettings
from src.track import Track
from src.tag import ThreadLyricsSearch
from src.tools import (
    TOKEN_URL,
    VERSION,
    LYRICS_LINES,
    ColorLight,
    CustomIcon,
    Mode,
    Settings,
    TrackLayout,
    Color_,
    State,
    IconTheme,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GTagger


class WindowMain(QtWidgets.QWidget):
    """
    Main window of the GUI.

    Args:
        gtagger (GTagger): GTagger application.

    Attributes:
        gtagger (GTagger): GTagger application.
        track_layouts (dict[Track, TrackLayout]): Layouts containing the informations of each tracks added by the user.
        window_settings (QtWidgets.QMainWindow): Settings window.
        settings (SettingsWindow): Settings.
        window_informations (QtWidgets.QMainWindow): Informations window.
        informations (InformationsWindow): Informations.
        window_help (QtWidgets.QMainWindow) : Help window.
        help (WindowHelp) : Help.
        thread_search_lyrics: (QtCore.QThread): Thread to search for the lyrics.
    """

    def __init__(self, gtagger: GTagger) -> None:
        super().__init__()

        self.gtagger: GTagger = gtagger

        self.track_layouts: dict[Track, TrackLayout] = {}

        self.window_settings: QtWidgets.QMainWindow = QtWidgets.QMainWindow(self)
        self.settings: WindowSettings = WindowSettings(
            self, self.gtagger, self.window_settings
        )

        self.window_informations: QtWidgets.QMainWindow = QtWidgets.QMainWindow(self)
        self.informations: WindowInformations = WindowInformations(
            self, self.window_informations
        )

        self.window_help: QtWidgets.QMainWindow = QtWidgets.QMainWindow(self)
        self.help: WindowHelp = WindowHelp(self, self.window_help)

        self.thread_search_lyrics: QtCore.QThread = QtCore.QThread()

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        # Setup the toolbar
        self.action_add_files = QtGui.QAction("Select files")
        self.action_add_files.setToolTip("Select files")

        self.action_add_folder = QtGui.QAction("Select a folder")
        self.action_add_folder.setToolTip("Select a folder")

        self.action_search_lyrics = QtGui.QAction("Search for the lyrics")
        self.action_search_lyrics.setToolTip("Search for the lyrics")
        self.action_search_lyrics.setEnabled(False)

        self.action_save_lyrics = QtGui.QAction("Save the lyrics")
        self.action_save_lyrics.setToolTip("Save the lyrics")
        self.action_save_lyrics.setEnabled(False)

        self.action_cancel_rows = QtGui.QAction("Cancel the modifications")
        self.action_cancel_rows.setToolTip("Cancel the modifications\nof selected rows")
        self.action_cancel_rows.setEnabled(False)

        self.action_remove_rows = QtGui.QAction("Remove rows")
        self.action_remove_rows.setToolTip("Remove selected rows")
        self.action_remove_rows.setEnabled(False)

        self.action_settings = QtGui.QAction("Settings")
        self.action_settings.setToolTip("Settings")

        self.action_informations = QtGui.QAction("Informations")
        self.action_informations.setToolTip("Informations")

        self.action_help = QtGui.QAction("Help")
        self.action_help.setToolTip("Help")

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred
        )

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
        self.tool_bar.addWidget(spacer)
        self.tool_bar.addAction(self.action_settings)
        self.tool_bar.addAction(self.action_informations)
        self.tool_bar.addAction(self.action_help)

        # Setup the input token
        self.input_token = QtWidgets.QLineEdit()
        self.input_token.setPlaceholderText("Enter your Genius client access token")
        self.input_token.setToolTip("Enter token")
        regex_epx = QtCore.QRegularExpression("[a-zA-Z0-9_-]{64}")
        self.validator = QtGui.QRegularExpressionValidator(regex_epx, self)
        self.input_token.setValidator(self.validator)

        self.button_token = QtWidgets.QPushButton()
        self.button_token.setToolTip("Get the token\non Genius website")

        # Setup the main layout of the files
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

        # Setup the status bar
        self.progression_bar = QtWidgets.QProgressBar()
        self.progression_bar.setMaximumWidth(300)
        self.progression_bar.setFixedHeight(25)

        self.button_mode = QtWidgets.QPushButton()

        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.addPermanentWidget(self.progression_bar)
        self.status_bar.addPermanentWidget(self.button_mode)

        self.layout_ = QtWidgets.QGridLayout(self)
        self.layout_.setMenuBar(self.tool_bar)
        self.layout_.addLayout(self.layout_main, 0, 0, 1, 1)
        self.layout_.addWidget(self.status_bar, 1, 0, 1, 1)
        self.layout_.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout_)
        self.setWindowTitle(f"GTagger ({VERSION})")

        self.setup_style()

        self.action_add_files.triggered.connect(lambda: self.add_files(False))
        self.action_add_folder.triggered.connect(lambda: self.add_files(True))
        self.action_search_lyrics.triggered.connect(self.search_lyrics)
        self.action_save_lyrics.triggered.connect(self.save_lyrics)
        self.action_cancel_rows.triggered.connect(self.cancel_rows)
        self.action_remove_rows.triggered.connect(self.remove_selected_layouts)
        self.action_settings.triggered.connect(self.open_settings)
        self.action_informations.triggered.connect(self.open_informations)
        self.action_help.triggered.connect(self.open_help)
        self.input_token.textChanged.connect(self.token_changed)
        self.button_token.clicked.connect(self.open_token_page)
        self.button_mode.clicked.connect(self.change_mode)

    def setup_style(self):
        """Sets up the custom colors and icons for diverse elements of the application."""
        mode = self.gtagger.mode

        # Setup the windows icons
        icon_window_main = CustomIcon(IconTheme.SHARP, "pricetag", Color_.black)
        self.setWindowIcon(icon_window_main)
        icon_window_settings = CustomIcon(IconTheme.SHARP, "settings", Color_.black)
        self.window_settings.setWindowIcon(icon_window_settings)
        icon_window_informations = CustomIcon(
            IconTheme.SHARP, "information-circle", Color_.black
        )
        self.window_informations.setWindowIcon(icon_window_informations)

        # Change the icons
        icon_add_files = CustomIcon(IconTheme.OUTLINE, "documents", ColorLight.green)
        icon_add_folder = CustomIcon(IconTheme.OUTLINE, "folder-open", ColorLight.green)
        icon_search_lyrics = CustomIcon(IconTheme.OUTLINE, "search", ColorLight.blue)
        icon_save_lyrics = CustomIcon(IconTheme.OUTLINE, "save", ColorLight.green)
        icon_cancel_rows = CustomIcon(
            IconTheme.OUTLINE, "arrow-undo", ColorLight.orange
        )
        icon_remove_rows = CustomIcon(
            IconTheme.OUTLINE, "remove-circle", ColorLight.red
        )
        icon_settings = CustomIcon(IconTheme.OUTLINE, "settings", ColorLight.grey)
        icon_informations = CustomIcon(
            IconTheme.OUTLINE, "information-circle", ColorLight.grey
        )
        icon_help = CustomIcon(IconTheme.OUTLINE, "help-circle", ColorLight.grey)
        icon_token = CustomIcon(IconTheme.OUTLINE, "open", Color_.yellow_genius)

        if mode == Mode.NORMAL:
            self.button_mode.setToolTip("Switch to compact mode")
            icon_mode = CustomIcon(IconTheme.OUTLINE, "contract", ColorLight.grey)
        elif mode == Mode.COMPACT:
            self.button_mode.setToolTip("Switch to normal mode")
            icon_mode = CustomIcon(IconTheme.OUTLINE, "expand", ColorLight.grey)

        self.action_add_files.setIcon(icon_add_files)
        self.action_add_folder.setIcon(icon_add_folder)
        self.action_search_lyrics.setIcon(icon_search_lyrics)
        self.action_save_lyrics.setIcon(icon_save_lyrics)
        self.action_cancel_rows.setIcon(icon_cancel_rows)
        self.action_remove_rows.setIcon(icon_remove_rows)
        self.action_settings.setIcon(icon_settings)
        self.action_informations.setIcon(icon_informations)
        self.action_help.setIcon(icon_help)
        self.button_token.setIcon(icon_token)
        self.button_mode.setIcon(icon_mode)

        # Change the cover placeholders and if needed,
        # as well as the lyrics color
        for track, track_layout in self.track_layouts.items():
            if not track_layout.selected:
                track_layout.label_cover.setPixmap(track.covers[mode])
                if track.lyrics_new != "":
                    track_layout.label_lyrics.setStyleSheet(
                        f"color: {ColorLight.green.value}"
                    )
                else:
                    track_layout.label_lyrics.setStyleSheet("")

        # Change the color of the token line edit
        self.token_changed()

        # Change the color of the links
        self.informations.set_texts(Color_.yellow_genius)

    def select_directories(self) -> str | None:
        """Asks user to select a directory.

        Returns:
            str: Path of the directory.
        """
        directory_dialog = QtWidgets.QFileDialog()
        directory = directory_dialog.getExistingDirectory(caption="Select folder")
        if directory == "":
            return None
        return directory

    def select_files(self) -> list[Path]:
        """Asks user to select one or multiple MP3 files.

        Returns:
            list[str]: Paths of the files.
        """
        file_dialog = QtWidgets.QFileDialog()
        files = file_dialog.getOpenFileNames(
            self, caption="Select files", filter="MP3 files (*.mp3)"
        )
        if len(files[0]) == 0:
            return []
        return [Path(file) for file in files[0]]

    def is_token_valid(self) -> bool:
        """Checks to see if the token is in a valid format.

        Genius client access token have a length of 64 characters, and may include letters, digits, '_' and '-'.

        Returns:
            bool: `True` if the token is valid.
        """
        validator_state = self.validator.validate(self.input_token.text(), 0)[0]
        return validator_state == QtGui.QValidator.State.Acceptable

    def increment_progression_bar(self) -> None:
        """Increments the progression bar by 1."""
        self.progression_bar.setValue(self.progression_bar.value() + 1)

    def set_maximum_progression_bar(self, list: list | dict) -> None:
        """Set the maximum of the progression bar.

        Args:
            list (list): List of elements.
        """
        maximum = len(list) - 1
        # The maximum must be at least 1 (occurs when the list has only one element)
        if maximum == 0:
            maximum = 1
            self.progression_bar.setValue(0)
        self.progression_bar.setMaximum(maximum)

    def remove_layout(self, track: Track, track_layout: TrackLayout) -> None:
        """Removes a track layout.

        Args:
            track (Track): Track to remove.
            track_layout (TrackLayout): Track layout to remove.
        """
        track_layout.frame.hide()
        self.layout_files.removeItem(track_layout)
        self.track_layouts.pop(track)

    @QtCore.Slot()
    def change_mode(self) -> None:
        """Changes the layout mode of the application."""
        # Update the button
        if self.gtagger.mode == Mode.COMPACT:
            self.gtagger.mode = Mode.NORMAL
            self.button_mode.setToolTip("Switch to compact mode")
            self.button_mode.setIcon(
                CustomIcon(IconTheme.OUTLINE, "contract", ColorLight.grey)
            )
        elif self.gtagger.mode == Mode.NORMAL:
            self.gtagger.mode = Mode.COMPACT
            self.button_mode.setToolTip("Switch to normal mode")
            self.button_mode.setIcon(
                CustomIcon(IconTheme.OUTLINE, "expand", ColorLight.grey)
            )

        # Update the GUI
        for track, track_layout_old in self.track_layouts.copy().items():
            track_layout_new = TrackLayout(track, track_layout_old.state, self.gtagger)
            self.remove_layout(track, track_layout_old)
            self.track_layouts[track] = track_layout_new
            self.layout_files.addLayout(track_layout_new)

        # Update the settings
        self.gtagger.settings_manager.set_setting(
            Settings.MODE.value, self.gtagger.mode.value
        )

    @QtCore.Slot()
    def add_files(self, select_directory: bool) -> None:
        """Adds the selected files to the table.

        Args:
            select_directory (bool): `True` if the user selected a directory.
        """
        # Construct the list of files
        files: list[Path] | None = []
        if select_directory:
            directory = self.select_directories()
            if directory is None:
                return
            if self.settings.checkbox_recursive.isChecked():
                files = list(Path(directory).rglob("*.mp3"))
            else:
                files = list(Path(directory).glob("*.mp3"))
        else:
            files = self.select_files()
            if len(files) == 0:
                return

        self.progression_bar.reset()
        self.set_maximum_progression_bar(files)
        for file in files:
            # Create the track and read its tags
            track = Track(file)
            track.signal_lyrics_changed.connect(self.lyrics_changed)
            tags_read = track.read_tags()

            # Skip the file if the tags could not be read
            if not tags_read:
                self.increment_progression_bar()
                continue

            # Add the layouts with the files' informations
            track_layout = TrackLayout(
                track,
                State.TAGS_READ,
                self.gtagger,
            )
            track_layout.signal_mouse_event.connect(self.selection_changed)
            self.track_layouts[track] = track_layout
            self.layout_files.addLayout(track_layout)

            self.increment_progression_bar()

    @QtCore.Slot()
    def search_lyrics(self) -> None:
        """Searches for the lyrics of the files."""
        token = self.input_token.text()
        self.thread_search_lyrics = ThreadLyricsSearch(
            token,
            self.track_layouts,
            self.settings.checkbox_overwrite.isChecked(),
            self.gtagger,
        )
        self.thread_search_lyrics.signal_lyrics_searched.connect(self.lyrics_searched)
        self.progression_bar.reset()
        self.set_maximum_progression_bar(self.track_layouts)
        self.thread_search_lyrics.start()

    @QtCore.Slot()
    def token_changed(self) -> None:
        """The token was changed by the user.

        Changes the color of the `QLineEdit` according to the new token,
        and toggles the search button accordingly.
        """
        if len(self.input_token.text()) == 0:
            # Input is empty
            self.input_token.setStyleSheet(f"border: 2px solid {ColorLight.red.value}")
            self.input_token.setToolTip("Enter token")
            self.action_search_lyrics.setEnabled(False)
        elif not self.is_token_valid():
            # Token is not valid
            self.input_token.setStyleSheet(f"border: 2px solid {ColorLight.red.value}")
            self.input_token.setToolTip("Invalid token")
            self.action_search_lyrics.setEnabled(False)
        else:
            # Token is valid
            self.input_token.setStyleSheet(
                f"border: 2px solid {ColorLight.green.value}"
            )
            self.input_token.setToolTip("Valid token")
            self.action_search_lyrics.setEnabled(True)

    @QtCore.Slot()
    def save_lyrics(self) -> None:
        """Saves the lyrics to the files."""
        for track, track_layout in self.track_layouts.items():
            saved = track.save_lyrics()
            if saved:
                track_layout.state_indicator.set_state(State.LYRICS_SAVED)
                track_layout.state_indicator.setToolTip(State.LYRICS_SAVED.value)
            else:
                track_layout.state_indicator.set_state(State.LYRICS_NOT_SAVED)
                track_layout.state_indicator.setToolTip(State.LYRICS_NOT_SAVED.value)
            track.read_tags()
            track.set_lyrics("")
            track_layout.label_lyrics.setText(
                track.get_lyrics(lines=LYRICS_LINES[self.gtagger.mode])
            )
            track_layout.label_lyrics.setToolTip("")

    @QtCore.Slot()
    def selection_changed(self) -> None:
        """The selection of the tracks changed.

        Toggles the cancel and remove buttons, and changes lyrics color.
        """
        enable_cancel = False
        enable_remove = False
        for track, track_layout in self.track_layouts.items():
            if track_layout.selected:
                if track.lyrics_new != "":
                    track_layout.label_lyrics.setStyleSheet(
                        f"color: {Color_.green.value}"
                    )
                enable_remove = True
                if track.lyrics_new != "":
                    enable_cancel = True
            else:
                if track.lyrics_new != "":
                    track_layout.label_lyrics.setStyleSheet(
                        f"color: {ColorLight.green.value}"
                    )
                else:
                    track_layout.label_lyrics.setStyleSheet("")
        self.action_cancel_rows.setEnabled(enable_cancel)
        self.action_remove_rows.setEnabled(enable_remove)

    @QtCore.Slot()
    def cancel_rows(self) -> None:
        """Removes the added lyrics from the files."""
        for track, track_layout in self.track_layouts.items():
            if track_layout.selected:
                track.set_lyrics("")
                track_layout.label_lyrics.setText(
                    track.get_lyrics(lines=LYRICS_LINES[self.gtagger.mode])
                )
                track_layout.label_lyrics.setToolTip("")

    @QtCore.Slot()
    def remove_selected_layouts(self) -> None:
        """Removes the selected layouts."""
        for track, track_layout in self.track_layouts.copy().items():
            if track_layout.selected:
                self.remove_layout(track, track_layout)
        self.selection_changed()

    @QtCore.Slot()
    def lyrics_changed(self) -> None:
        """The lyrics of a track changed.

        Changes the color of the lyrics according to the current theme.
        """
        enable_save = False
        for track, track_layout in self.track_layouts.items():
            if track.lyrics_new != "":
                enable_save = True
                if track_layout.selected:
                    track_layout.label_lyrics.setStyleSheet(
                        f"color: {Color_.green.value}"
                    )
                else:
                    track_layout.label_lyrics.setStyleSheet(
                        f"color: {ColorLight.green.value}"
                    )
            else:
                track_layout.label_lyrics.setStyleSheet("")
        self.action_save_lyrics.setEnabled(enable_save)

    @QtCore.Slot()
    def lyrics_searched(self) -> None:
        """The lyrics of a track have been searched."""
        self.increment_progression_bar()

    @QtCore.Slot()
    def open_token_page(self) -> None:
        """Opens the Genius website to fetch the client access token."""
        QtGui.QDesktopServices.openUrl(TOKEN_URL)

    @QtCore.Slot()
    def open_settings(self) -> None:
        """Opens the settings window."""
        self.window_settings.show()

    @QtCore.Slot()
    def open_informations(self) -> None:
        """Opens the informations window."""
        self.window_informations.show()

    @QtCore.Slot()
    def open_help(self) -> None:
        """Opens the help window."""
        self.window_help.show()
