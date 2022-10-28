"""Application's main window.

Handles the creation of the main window and the interactions with the user.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6 import QtCore, QtGui, QtWidgets

from src.tag import ThreadSearchLyrics, ThreadTrackRead
from src.track import Track
from src.track_layout import TrackLayout
from src.utils import (
    LYRICS_LINES,
    TOKEN_URL,
    VERSION,
    Color_,
    FileType,
    Mode,
    Settings,
    State,
    get_icon,
)
from src.window_help import WindowHelp
from src.window_informations import WindowInformations
from src.window_settings import WindowSettings

if TYPE_CHECKING:
    from gtagger import GTagger


class WindowMain(QtWidgets.QWidget):
    """
    Main window of the GUI.

    Args:
        gtagger (GTagger): GTagger application.

    Attributes:
        gtagger (GTagger): GTagger application.
        track_layouts (dict[Track, TrackLayout]): Layouts containing
        the information of each track added by the user.
        window_settings (WindowSettings): Settings window.
        window_informations (WindowInformations): Informations window.
        window_help (WindowHelp) : Help window.
        thread_search_lyrics: (ThreadLyricsSearch): Thread to search for the lyrics.
    """

    lock = threading.Lock()

    def __init__(self, gtagger: GTagger) -> None:
        super().__init__()

        self.gtagger: GTagger = gtagger
        self.track_layouts: dict[Track, TrackLayout] = {}
        self.window_settings: WindowSettings = WindowSettings(self, self.gtagger)
        self.window_informations: WindowInformations = WindowInformations(self)
        self.window_help: WindowHelp = WindowHelp(self)
        self.thread_add_files: ThreadTrackRead = None
        self.thread_search_lyrics: ThreadSearchLyrics = None

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        # Toolbar
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

        # Token input
        self.input_token = QtWidgets.QLineEdit()
        self.input_token.setPlaceholderText("Enter your Genius client access token")
        self.input_token.setToolTip("Enter token")
        regex = QtCore.QRegularExpression("[a-zA-Z0-9_-]{64}")
        self.validator = QtGui.QRegularExpressionValidator(regex, self)
        self.input_token.setValidator(self.validator)

        # Button to open the Genius website
        self.button_token = QtWidgets.QPushButton()
        self.button_token.setToolTip("Get the token on Genius website")

        # Separator
        self.frame_separator = QtWidgets.QFrame()
        self.frame_separator.setFrameStyle(
            QtWidgets.QFrame.HLine | QtWidgets.QFrame.Plain
        )

        # Text filter input
        self.input_filter_text = QtWidgets.QLineEdit()
        self.input_filter_text.setPlaceholderText("Filter by title or artist")
        self.input_filter_text.setToolTip("Enter text")

        # Has lyrics filter
        self.button_filter_lyrics = QtWidgets.QPushButton()
        self.button_filter_lyrics.setToolTip("Hide files with lyrics")
        self.button_filter_lyrics.setCheckable(True)
        self.button_filter_lyrics.setChecked(True)

        # Main layout of the files
        self.layout_files = QtWidgets.QVBoxLayout()
        self.layout_files.setAlignment(QtCore.Qt.AlignTop)
        self.layout_files.setContentsMargins(0, 0, 5, 0)
        self.layout_files.setSpacing(5)

        self.widget_files = QtWidgets.QWidget()
        self.widget_files.setLayout(self.layout_files)

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.widget_files)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.layout_main = QtWidgets.QGridLayout()
        self.layout_main.addWidget(self.input_token, 0, 0, 1, 1)
        self.layout_main.addWidget(self.button_token, 0, 1, 1, 1)
        self.layout_main.addWidget(self.input_filter_text, 1, 0, 1, 1)
        self.layout_main.addWidget(self.button_filter_lyrics, 1, 1, 1, 1)
        self.layout_main.addWidget(self.frame_separator, 2, 0, 1, 2)
        self.layout_main.addWidget(self.scroll_area, 3, 0, 1, 2)
        self.layout_main.setContentsMargins(5, 5, 5, 0)

        # Status bar
        self.progression_bar = QtWidgets.QProgressBar()
        self.progression_bar.setMaximumWidth(300)
        self.progression_bar.setFixedHeight(25)

        self.button_stop_search = QtWidgets.QPushButton()
        self.button_stop_search.setEnabled(False)
        self.button_stop_search.setToolTip("Stop searching")
        self.button_change_mode = QtWidgets.QPushButton()

        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.addPermanentWidget(self.progression_bar)
        self.status_bar.addPermanentWidget(self.button_stop_search)
        self.status_bar.addPermanentWidget(self.button_change_mode)

        # Main window
        self.layout_ = QtWidgets.QGridLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setMenuBar(self.tool_bar)
        self.layout_.addLayout(self.layout_main, 0, 0, 1, 1)
        self.layout_.addWidget(self.status_bar, 1, 0, 1, 1)

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
        self.input_filter_text.returnPressed.connect(self.filter)
        self.button_filter_lyrics.clicked.connect(self.filter)
        self.button_stop_search.clicked.connect(self.stop_search)
        self.button_change_mode.clicked.connect(self.change_mode)

    def setup_style(self):
        """Sets up the custom colors and icons for diverse elements of the application."""
        mode = self.gtagger.mode

        # Set up the windows icons
        icon_window_main = get_icon("tag-multiple", color=Color_.yellow_genius.value)
        icon_window_settings = get_icon("cog", color="black")
        icon_window_information = get_icon("information", color="black")
        icon_window_help = get_icon("help-circle", color="black")
        self.setWindowIcon(icon_window_main)
        self.window_settings.setWindowIcon(icon_window_settings)
        self.window_informations.setWindowIcon(icon_window_information)
        self.window_help.setWindowIcon(icon_window_help)

        # Change the icons
        icon_add_files = get_icon("file-outline")
        icon_add_folder = get_icon("folder-open")
        icon_search_lyrics = get_icon("magnify", color=Color_.light_blue.value)
        icon_save_lyrics = get_icon("content-save", color=Color_.light_green.value)
        icon_cancel_rows = get_icon("backup-restore", color=Color_.orange.value)
        icon_remove_rows = get_icon("minus-circle", color=Color_.red.value)
        icon_settings = get_icon("cog")
        icon_information = get_icon("information")
        icon_help = get_icon("help-circle")
        icon_token = get_icon("launch", color_active=Color_.yellow_genius.value)
        icon_filter_lyrics = get_icon("format-letter-case")
        icon_stop_search = get_icon("stop", color=Color_.red.value)
        if mode == Mode.NORMAL:
            self.button_change_mode.setToolTip("Switch to compact mode")
            icon_change_mode = get_icon("arrow-expand")
        elif mode == Mode.COMPACT:
            self.button_change_mode.setToolTip("Switch to normal mode")
            icon_change_mode = get_icon("arrow-collapse")

        self.action_add_files.setIcon(icon_add_files)
        self.action_add_folder.setIcon(icon_add_folder)
        self.action_search_lyrics.setIcon(icon_search_lyrics)
        self.action_save_lyrics.setIcon(icon_save_lyrics)
        self.action_cancel_rows.setIcon(icon_cancel_rows)
        self.action_remove_rows.setIcon(icon_remove_rows)
        self.action_settings.setIcon(icon_settings)
        self.action_informations.setIcon(icon_information)
        self.action_help.setIcon(icon_help)
        self.button_token.setIcon(icon_token)
        self.button_filter_lyrics.setIcon(icon_filter_lyrics)
        self.button_stop_search.setIcon(icon_stop_search)
        self.button_change_mode.setIcon(icon_change_mode)

        # Change the cover placeholders and if needed,
        # as well as the lyrics color
        for track, track_layout in self.track_layouts.items():
            if not track_layout.selected:
                track_layout.label_cover.setPixmap(track.covers[mode])
                if track.lyrics_new != "":
                    track_layout.label_lyrics.setStyleSheet(
                        f"color: {Color_.light_green.value}"
                    )
                else:
                    track_layout.label_lyrics.setStyleSheet("")

        # Change the color of the token line edit
        self.token_changed()

        # Change the color of the links
        self.window_informations.set_texts(Color_.yellow_genius)

    @staticmethod
    def select_directories() -> str | None:
        """Asks the user to select a directory.

        Returns:
            str: Path of the directory.
        """
        directory_dialog = QtWidgets.QFileDialog()
        directory = directory_dialog.getExistingDirectory(caption="Select folder")
        if directory == "":
            return None
        return directory

    def select_files(self) -> list[Path]:
        """Asks the user to select one or multiple MP3 files.

        Returns:
            list[str]: Paths of the files.
        """
        file_dialog = QtWidgets.QFileDialog()
        files = file_dialog.getOpenFileNames(
            self, caption="Select files", filter="Audio files (*.mp3 *.flac)"
        )
        if len(files[0]) == 0:
            return []
        return [Path(file) for file in files[0]]

    def is_token_valid(self) -> bool:
        """Checks to see if the token is in a valid format.

        Genius client access token have a length of 64 characters,
        and may include letters, digits, '_' and '-'.

        Returns:
            bool: `True` if the token is valid.
        """
        validator_state: QtGui.QValidator.State = self.validator.validate(
            self.input_token.text(), 0
        )[0]
        return validator_state == QtGui.QValidator.State.Acceptable

    def increment_progression_bar(self) -> None:
        """Increments the progression bar by 1."""
        self.progression_bar.setValue(self.progression_bar.value() + 1)

    def set_maximum_progression_bar(self, list_: list | dict) -> None:
        """Set the maximum of the progression bar.

        Args:
            list_ (list | dict): List of elements.
        """
        maximum = len(list_) - 1
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
        self.layout_files.removeWidget(track_layout)
        self.track_layouts.pop(track)

    @QtCore.Slot()
    def change_mode(self) -> None:
        """Changes the layout mode of the application."""
        # Update the button
        if self.gtagger.mode == Mode.COMPACT:
            self.gtagger.mode = Mode.NORMAL
            self.button_change_mode.setToolTip("Switch to compact mode")
            self.button_change_mode.setIcon(get_icon("arrow-collapse"))
        elif self.gtagger.mode == Mode.NORMAL:
            self.gtagger.mode = Mode.COMPACT
            self.button_change_mode.setToolTip("Switch to normal mode")
            self.button_change_mode.setIcon(get_icon("arrow-expand"))

        # Update the GUI
        for track, track_layout_old in self.track_layouts.copy().items():
            track_layout_new = TrackLayout(track, track_layout_old.state, self.gtagger)
            track_layout_new.signal_mouse_event.connect(self.selection_changed)
            self.remove_layout(track, track_layout_old)
            self.track_layouts[track] = track_layout_new
            self.layout_files.addWidget(track_layout_new)

        # Apply all the filters
        self.filter()

        # Update the settings
        self.gtagger.settings_manager.set_setting(
            Settings.MODE.value, self.gtagger.mode.value
        )

    @QtCore.Slot()
    def add_files(self, select_directory: bool) -> None:
        """Adds the selected tracks to the scroll area.

        Args:
            select_directory (bool): `True` if the user selected a directory.
        """
        # Construct the list of files
        files: list[Path] = []
        if select_directory:
            directory = self.select_directories()
            if directory is None:
                return
            if self.window_settings.checkbox_recursive.isChecked():
                for file_type in FileType:
                    files.extend(list(Path(directory).rglob("*." + file_type.value)))
            else:
                for file_type in FileType:
                    files.extend(list(Path(directory).glob("*." + file_type.value)))
        else:
            files = self.select_files()
        if len(files) <= 0:
            return

        self.progression_bar.reset()
        self.set_maximum_progression_bar(files)

        self.thread_add_files = ThreadTrackRead(
            files, self.action_add_files, self.action_add_folder, self.gtagger
        )
        self.thread_add_files.add_track.connect(self.add_track)
        self.thread_add_files.start()

    @QtCore.Slot()
    def add_track(self, track: Track):
        """Adds the track `track` to the scroll area.

        Args:
            track (Track): Track to add.
        """
        # Handle only one track at a time
        with WindowMain.lock:
            # Skip the file if the tags could not be read
            if track is None:
                self.increment_progression_bar()
                return

            # Create the track layout and add it
            track_layout = TrackLayout(
                track,
                State.TAGS_READ,
                self.gtagger,
            )
            track.signal_lyrics_changed.connect(self.lyrics_changed)
            track_layout.signal_mouse_event.connect(self.selection_changed)
            self.track_layouts[track] = track_layout
            self.layout_files.addWidget(track_layout)
            self.increment_progression_bar()

    @QtCore.Slot()
    def search_lyrics(self) -> None:
        """Searches for the lyrics of the files."""
        self.thread_search_lyrics = ThreadSearchLyrics(
            self.input_token.text(),
            self.track_layouts,
            self.window_settings.checkbox_overwrite.isChecked(),
            self.button_stop_search,
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
            self.input_token.setStyleSheet(
                f"border: 2px solid {Color_.light_red.value}"
            )
            self.input_token.setToolTip("Enter token")
            self.action_search_lyrics.setEnabled(False)
        elif not self.is_token_valid():
            # Token is not valid
            self.input_token.setStyleSheet(
                f"border: 2px solid {Color_.light_red.value}"
            )
            self.input_token.setToolTip("Invalid token")
            self.action_search_lyrics.setEnabled(False)
        else:
            # Token is valid
            self.input_token.setStyleSheet(
                f"border: 2px solid {Color_.light_green.value}"
            )
            self.input_token.setToolTip("Valid token")
            self.action_search_lyrics.setEnabled(len(self.track_layouts) > 0)

    @QtCore.Slot()
    def save_lyrics(self) -> None:
        """Saves the lyrics to the files."""
        self.progression_bar.reset()
        self.set_maximum_progression_bar(self.track_layouts)
        for track, track_layout in self.track_layouts.items():
            saved = track.save_lyrics()
            if saved:
                track_layout.state_indicator.set_state(State.LYRICS_SAVED)
                track_layout.state_indicator.setToolTip(State.LYRICS_SAVED.value)
                track_layout.state = State.LYRICS_SAVED
                track.read_tags()
                track.set_lyrics_new("")
                track_layout.label_lyrics.setText(
                    track.get_lyrics(lines=LYRICS_LINES[self.gtagger.mode])
                )
                track_layout.label_lyrics.setToolTip(track.get_lyrics_original())
            else:
                track_layout.state_indicator.set_state(State.LYRICS_NOT_SAVED)
                track_layout.state_indicator.setToolTip(State.LYRICS_NOT_SAVED.value)
                track_layout.state = State.LYRICS_NOT_SAVED
            self.increment_progression_bar()

    @QtCore.Slot()
    def cancel_rows(self) -> None:
        """Removes the added lyrics from the files."""
        for track, track_layout in self.track_layouts.items():
            if track_layout.selected:
                track.set_lyrics_new("")
                track_layout.label_lyrics.setText(
                    track.get_lyrics(lines=LYRICS_LINES[self.gtagger.mode])
                )
                track_layout.label_lyrics.setToolTip(track.get_lyrics_original())
                track_layout.state_indicator.set_state(State.TAGS_READ)
                track_layout.state_indicator.setToolTip(State.TAGS_READ.value)
                track_layout.state = State.TAGS_READ

    @QtCore.Slot()
    def remove_selected_layouts(self) -> None:
        """Removes the selected layouts."""
        for track, track_layout in self.track_layouts.copy().items():
            if track_layout.selected:
                self.remove_layout(track, track_layout)
        self.selection_changed()

    @QtCore.Slot()
    def selection_changed(self) -> None:
        """The selection of the tracks changed.

        Toggles the cancel and remove buttons, and changes lyrics color.
        """
        enable_cancel = False
        enable_remove = False
        for track, track_layout in self.track_layouts.items():
            if track_layout.selected:
                enable_remove = True
                if track.has_lyrics_new():
                    enable_cancel = True
        self.action_cancel_rows.setEnabled(enable_cancel)
        self.action_remove_rows.setEnabled(enable_remove)

    @QtCore.Slot()
    def lyrics_changed(self) -> None:
        """The lyrics of a track changed."""
        enable_save = False
        for track, track_layout in self.track_layouts.items():
            if track.has_lyrics_new():
                # Track has new lyrics
                enable_save = True
                track_layout.label_lyrics.setStyleSheet(
                    f"color: {Color_.light_green.value}"
                )
            else:
                track_layout.label_lyrics.setStyleSheet("")
        self.action_save_lyrics.setEnabled(enable_save)
        self.selection_changed()  # Update the cancel and remove buttons

    @QtCore.Slot()
    def filter(self) -> None:
        """Applies the filters to the track layouts."""
        show_lyrics = self.button_filter_lyrics.isChecked()
        text = self.input_filter_text.text()

        # Apply the filters
        for track, track_layout in self.track_layouts.items():
            visible = False
            if show_lyrics:
                if text in track.get_title() or text in track.get_artists():
                    visible = True
            elif not track.has_lyrics_original():
                if text in track.get_title() or text in track.get_artists():
                    visible = True
            track_layout.setVisible(visible)

        # Update the lyrics filter button
        if show_lyrics:
            self.button_filter_lyrics.setToolTip("Hide files with lyrics")
        else:
            self.button_filter_lyrics.setToolTip("Show files with lyrics")

    @QtCore.Slot()
    def stop_search(self) -> None:
        """Stop searching for the lyrics."""
        if self.thread_search_lyrics.isRunning():
            self.thread_search_lyrics.stop_search = True
            self.button_stop_search.setEnabled(False)

    @QtCore.Slot()
    def lyrics_searched(self) -> None:
        """The lyrics of a track have been searched."""
        self.increment_progression_bar()

    @staticmethod
    @QtCore.Slot()
    def open_token_page() -> None:
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

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Intercepts the close event of the main window.

        If it is running, waits for `ThreadLyricsSearch` to quit before exiting the application.

        Args:
            event (QtGui.QCloseEvent): Close event.
        """
        if (
            self.thread_search_lyrics is not None
            and self.thread_search_lyrics.isRunning()
        ):
            self.thread_search_lyrics.stop_search = True
            self.thread_search_lyrics.wait()
        event.accept()
