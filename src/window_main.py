"""Application's main window.

Handles the creation of the main window and the interactions with the user.
"""

from __future__ import annotations

import threading
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6 import QtCore, QtGui, QtWidgets

from src.consts import (
    HEIGHT_PROGRESS_BAR,
    LINES_LYRICS,
    MARGIN_TRACK_LAYOUT,
    MARGIN_CENTRAL_WIDGET,
    SIZE_BUTTON,
    SIZE_ICON,
    SIZE_ICON_TOOL_BAR,
    URL_TOKEN,
    VERSION,
    WIDTH_PROGRESS_BAR,
)
from src.enums import CustomColors, FileType, Sort, State
from src.icons import get_icon
from src.tag import ThreadReadTracks, ThreadSearchLyrics
from src.track import Track
from src.track_layout import TrackLayout
from src.tracks_list import CustomListWidgetItem
from src.window_help import WindowHelp
from src.window_information import WindowInformation
from src.window_settings import WindowSettings

if TYPE_CHECKING:
    from gtagger import GTagger


class WindowMain(QtWidgets.QMainWindow):
    """
    Main window of the GUI.

    Attributes:
        gtagger (GTagger): GTagger application.
        track_layouts_items (dict[Track, tuple[TrackLayout, CustomListWidgetItem]]): Layouts and items containing the information of each track added by the user.
        window_settings (WindowSettings): Settings window.
        window_information (WindowInformation): Information window.
        window_help (WindowHelp) : Help window.
        thread_add_files: (ThreadReadTracks): Thread to read the tracks.
        thread_search_lyrics: (ThreadLyricsSearch): Thread to search for the lyrics.
        self.sort (Sort): Sort mode for the list of tracks.
    """

    lock = threading.Lock()

    def __init__(self, gtagger: GTagger) -> None:
        """Init WindowMain.

        Args:
            gtagger (GTagger): GTagger application.
        """
        super().__init__()

        self.gtagger: GTagger = gtagger
        self.track_layouts_items: dict[
            Track, tuple[TrackLayout, CustomListWidgetItem]
        ] = {}
        self.window_settings: WindowSettings = WindowSettings(self, self.gtagger)
        self.window_information: WindowInformation = WindowInformation(self)
        self.window_help: WindowHelp = WindowHelp(self)
        self.thread_read_tracks: ThreadReadTracks
        self.thread_search_lyrics: ThreadSearchLyrics
        self.sort: Sort = Sort.ASCENDING

        self.setup_ui()

    def setup_ui(self) -> None:
        """Set up the UI of the window."""
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

        self.action_information = QtGui.QAction("Information")
        self.action_information.setToolTip("Information")

        self.action_help = QtGui.QAction("Help")
        self.action_help.setToolTip("Help")

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )

        self.tool_bar = QtWidgets.QToolBar()
        self.tool_bar.setIconSize(SIZE_ICON_TOOL_BAR)
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
        self.tool_bar.addAction(self.action_information)
        self.tool_bar.addAction(self.action_help)

        # Token input
        self.input_token = QtWidgets.QLineEdit()
        self.input_token.setClearButtonEnabled(True)
        self.input_token.setPlaceholderText("Enter your Genius client access token")
        self.input_token.setToolTip("Enter token")
        regex = QtCore.QRegularExpression("[a-zA-Z0-9_-]{64}")
        self.validator = QtGui.QRegularExpressionValidator(regex, self)
        self.input_token.setValidator(self.validator)
        self.input_token.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )

        # Button to open the Genius website
        self.button_token = QtWidgets.QPushButton()
        self.button_token.setToolTip("Get the token on Genius website")
        self.button_token.setFixedSize(SIZE_BUTTON, SIZE_BUTTON)
        self.button_token.setStyleSheet(f"""icon-size: {SIZE_ICON}px""")

        # Text filter input
        self.input_filter_text = QtWidgets.QLineEdit()
        self.input_filter_text.setClearButtonEnabled(True)
        self.input_filter_text.setPlaceholderText("Filter by title or artist")
        self.input_filter_text.setToolTip("Enter text")
        self.input_filter_text.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum
        )

        # Has lyrics filter
        self.button_filter_lyrics = QtWidgets.QPushButton()
        self.button_filter_lyrics.setToolTip("Show files with lyrics")
        self.button_filter_lyrics.setCheckable(True)
        self.button_filter_lyrics.setChecked(True)
        self.button_filter_lyrics.setFixedSize(SIZE_BUTTON, SIZE_BUTTON)
        self.button_filter_lyrics.setStyleSheet(f"""icon-size: {SIZE_ICON}px""")

        # Case filter
        self.button_filter_case = QtWidgets.QPushButton()
        self.button_filter_case.setToolTip("Match case")
        self.button_filter_case.setCheckable(True)
        self.button_filter_case.setChecked(False)
        self.button_filter_case.setFixedSize(SIZE_BUTTON, SIZE_BUTTON)
        self.button_filter_case.setStyleSheet(f"""icon-size: {SIZE_ICON}px""")

        # Title sort
        self.button_sort_title = QtWidgets.QPushButton()
        self.button_sort_title.setToolTip("Sort based on title")
        self.button_sort_title.setFixedSize(SIZE_BUTTON, SIZE_BUTTON)
        self.button_sort_title.setStyleSheet(f"""icon-size: {SIZE_ICON}px""")

        # List of the tracks
        self.list_tracks = QtWidgets.QListWidget()
        self.list_tracks.setSortingEnabled(True)
        self.list_tracks.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.list_tracks.setStyleSheet(
            """QListWidget::item {margin-bottom: """
            + str(MARGIN_TRACK_LAYOUT)
            + """px; margin-right: """
            + str(MARGIN_TRACK_LAYOUT)
            + """px;}"""
        )

        # Scroll are for the list of tracks
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.list_tracks)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        # Central widget's layout
        self.layout_widget_central = QtWidgets.QGridLayout()
        self.layout_widget_central.addWidget(self.input_token, 0, 0, 1, 3)
        self.layout_widget_central.addWidget(self.button_token, 0, 3, 1, 1)
        self.layout_widget_central.addWidget(self.input_filter_text, 1, 0, 1, 1)
        self.layout_widget_central.addWidget(self.button_filter_lyrics, 1, 1, 1, 1)
        self.layout_widget_central.addWidget(self.button_filter_case, 1, 2, 1, 1)
        self.layout_widget_central.addWidget(self.button_sort_title, 1, 3, 1, 1)
        self.layout_widget_central.addWidget(self.scroll_area, 3, 0, 1, 4)
        self.layout_widget_central.setContentsMargins(MARGIN_CENTRAL_WIDGET)

        # Central widget
        self.widget_central = QtWidgets.QWidget()
        self.widget_central.setLayout(self.layout_widget_central)

        # Progression bar
        self.progression_bar = QtWidgets.QProgressBar()
        self.progression_bar.setMaximumWidth(WIDTH_PROGRESS_BAR)
        self.progression_bar.setFixedHeight(HEIGHT_PROGRESS_BAR)

        # Button stop search
        self.button_stop_search = QtWidgets.QPushButton()
        self.button_stop_search.setEnabled(False)
        self.button_stop_search.setToolTip("Stop searching")
        self.button_stop_search.setStyleSheet(f"""icon-size: {SIZE_ICON}px""")

        # Status bar
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.addPermanentWidget(self.progression_bar)
        self.status_bar.addPermanentWidget(self.button_stop_search)

        # Main window
        self.setWindowTitle(f"GTagger ({VERSION})")
        self.setCentralWidget(self.widget_central)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.tool_bar)
        self.setStatusBar(self.status_bar)

        self.setup_style()

        self.action_add_files.triggered.connect(lambda: self.add_files(False))
        self.action_add_folder.triggered.connect(lambda: self.add_files(True))
        self.action_search_lyrics.triggered.connect(self.search_lyrics)
        self.action_save_lyrics.triggered.connect(self.save_lyrics)
        self.action_cancel_rows.triggered.connect(self.cancel_rows)
        self.action_remove_rows.triggered.connect(self.remove_selected_layouts)
        self.action_settings.triggered.connect(self.open_settings)
        self.action_information.triggered.connect(self.open_information)
        self.action_help.triggered.connect(self.open_help)
        self.input_token.textChanged.connect(self.token_changed)
        self.button_token.clicked.connect(self.open_token_page)
        self.input_filter_text.textChanged.connect(self.filter_tracks)
        self.button_filter_lyrics.clicked.connect(self.filter_tracks)
        self.button_filter_case.clicked.connect(self.filter_tracks)
        self.button_sort_title.clicked.connect(self.sort_tracks)
        self.button_stop_search.clicked.connect(self.stop_search)

    def setup_style(self):
        """Set up the custom colors and icons for diverse elements of the application."""
        # Set up the windows icons
        icon_window_main = get_icon(
            "tag-multiple", color=CustomColors.YELLOW_GENIUS.value
        )
        icon_window_settings = get_icon("cog", color="black")
        icon_window_information = get_icon("information", color="black")
        icon_window_help = get_icon("help-circle", color="black")
        self.setWindowIcon(icon_window_main)
        self.window_settings.setWindowIcon(icon_window_settings)
        self.window_information.setWindowIcon(icon_window_information)
        self.window_help.setWindowIcon(icon_window_help)

        # Change the icons
        icon_add_files = get_icon("file-outline")
        icon_add_folder = get_icon("folder-open")
        icon_search_lyrics = get_icon("magnify", color=CustomColors.LIGHT_BLUE.value)
        icon_save_lyrics = get_icon(
            "content-save", color=CustomColors.LIGHT_GREEN.value
        )
        icon_cancel_rows = get_icon("backup-restore", color=CustomColors.ORANGE.value)
        icon_remove_rows = get_icon("minus-circle", color=CustomColors.RED.value)
        icon_settings = get_icon("cog")
        icon_information = get_icon("information")
        icon_help = get_icon("help-circle")
        icon_token = get_icon("launch", color_active=CustomColors.YELLOW_GENIUS.value)
        icon_filter_lyrics = get_icon("file-music-outline")
        icon_filter_case = get_icon("format-letter-case")
        self.icon_sort_title_ascending = get_icon("sort-alphabetical-ascending")
        self.icon_sort_title_descending = get_icon("sort-alphabetical-descending")
        icon_stop_search = get_icon("stop", color=CustomColors.RED.value)

        self.action_add_files.setIcon(icon_add_files)
        self.action_add_folder.setIcon(icon_add_folder)
        self.action_search_lyrics.setIcon(icon_search_lyrics)
        self.action_save_lyrics.setIcon(icon_save_lyrics)
        self.action_cancel_rows.setIcon(icon_cancel_rows)
        self.action_remove_rows.setIcon(icon_remove_rows)
        self.action_settings.setIcon(icon_settings)
        self.action_information.setIcon(icon_information)
        self.action_help.setIcon(icon_help)
        self.button_token.setIcon(icon_token)
        self.button_filter_lyrics.setIcon(icon_filter_lyrics)
        self.button_filter_case.setIcon(icon_filter_case)
        self.button_sort_title.setIcon(self.icon_sort_title_ascending)
        self.button_stop_search.setIcon(icon_stop_search)

        # Change the cover placeholders and if needed,
        # as well as the lyrics color
        for track, layout_item in self.track_layouts_items.items():
            track_layout = layout_item[0]
            if not track_layout.selected:
                track_layout.label_cover.setPixmap(track.cover)
                if track.lyrics_new != "":
                    track_layout.label_lyrics.setStyleSheet(
                        f"color: {CustomColors.LIGHT_GREEN.value}"
                    )
                else:
                    track_layout.label_lyrics.setStyleSheet("")

        # Change the color of the token line edit
        self.token_changed()

        # Change the color of the links
        self.window_information.set_texts(CustomColors.YELLOW_GENIUS)

    @staticmethod
    def select_directories() -> str | None:
        """Asks the user to select a directory.

        Returns None if the user cancels.

        Returns:
            str | None: Path of the directory.
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
        """Check to see if the token is in a valid format.

        Genius client access token have a length of 64 characters,
        and may include letters, digits, '_' and '-'.

        Returns:
            bool: `True` if the token is valid.
        """
        validate = self.validator.validate(self.input_token.text(), 0)
        # validate() returns an untyped object
        return validate[0] == QtGui.QValidator.State.Acceptable  # type: ignore

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

    def remove_layout(self, track: Track, item: CustomListWidgetItem) -> None:
        """Remove a track item.

        Args:
            track (Track): Track to remove.
            item (CustomListWidgetItem): Track item to remove.
        """
        self.list_tracks.takeItem(self.list_tracks.row(item))
        self.track_layouts_items.pop(track)

    @QtCore.Slot()
    def add_files(self, select_directory: bool) -> None:
        """Add the selected tracks to the scroll area.

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

        self.thread_read_tracks = ThreadReadTracks(
            files, self.action_add_files, self.action_add_folder, self.gtagger
        )
        self.thread_read_tracks.add_track.connect(self.add_track)
        self.thread_read_tracks.start()

    @QtCore.Slot()
    def add_track(self, track: Track):
        """Add the track `track` to the scroll area.

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
            layout = TrackLayout(
                track,
                State.TAGS_READ,
                self.gtagger,
            )
            track.signal_lyrics_changed.connect(self.lyrics_changed)
            layout.signal_mouse_event.connect(self.selection_changed)
            item = CustomListWidgetItem(track.get_title(), self.list_tracks)
            item.setSizeHint(layout.sizeHint())
            self.list_tracks.addItem(item)
            self.list_tracks.setItemWidget(item, layout)
            self.track_layouts_items[track] = (layout, item)
            self.increment_progression_bar()

    @QtCore.Slot()
    def search_lyrics(self) -> None:
        """Search for the lyrics of the files."""
        self.thread_search_lyrics = ThreadSearchLyrics(
            self.input_token.text(),
            self.track_layouts_items,
            self.window_settings.checkbox_overwrite.isChecked(),
            self.button_stop_search,
            self.gtagger,
        )
        self.thread_search_lyrics.signal_lyrics_searched.connect(self.lyrics_searched)
        self.progression_bar.reset()
        self.set_maximum_progression_bar(self.track_layouts_items)
        self.thread_search_lyrics.start()

    @QtCore.Slot()
    def token_changed(self) -> None:
        """Token changed by the user.

        Change the color of the `QLineEdit` according to the new token,
        and toggles the search button accordingly.
        """
        if len(self.input_token.text()) == 0:
            # Input is empty
            self.input_token.setStyleSheet(
                f"border: 2px solid {CustomColors.LIGHT_RED.value}"
            )
            self.input_token.setToolTip("Enter token")
            self.action_search_lyrics.setEnabled(False)
        elif not self.is_token_valid():
            # Token is not valid
            self.input_token.setStyleSheet(
                f"border: 2px solid {CustomColors.LIGHT_RED.value}"
            )
            self.input_token.setToolTip("Invalid token")
            self.action_search_lyrics.setEnabled(False)
        else:
            # Token is valid
            self.input_token.setStyleSheet(
                f"border: 2px solid {CustomColors.LIGHT_GREEN.value}"
            )
            self.input_token.setToolTip("Valid token")
            self.action_search_lyrics.setEnabled(len(self.track_layouts_items) > 0)

    @QtCore.Slot()
    def save_lyrics(self) -> None:
        """Save the lyrics to the files."""
        self.progression_bar.reset()
        self.set_maximum_progression_bar(self.track_layouts_items)
        for track, layout_item in self.track_layouts_items.items():
            layout = layout_item[0]
            saved = track.save_lyrics()
            if saved:
                layout.state_indicator.set_state(State.LYRICS_SAVED)
                layout.state_indicator.setToolTip(State.LYRICS_SAVED.value)
                layout.state = State.LYRICS_SAVED
                track.read_tags()
                track.set_lyrics_new("")
                layout.label_lyrics.setText(track.get_lyrics(lines=LINES_LYRICS))
                layout.label_lyrics.setToolTip(track.get_lyrics_original())
            else:
                layout.state_indicator.set_state(State.LYRICS_NOT_SAVED)
                layout.state_indicator.setToolTip(State.LYRICS_NOT_SAVED.value)
                layout.state = State.LYRICS_NOT_SAVED
            self.increment_progression_bar()

    @QtCore.Slot()
    def cancel_rows(self) -> None:
        """Remove the added lyrics from the files."""
        for track, layout_item in self.track_layouts_items.items():
            layout = layout_item[0]
            if layout.selected:
                track.set_lyrics_new("")
                layout.label_lyrics.setText(track.get_lyrics(lines=LINES_LYRICS))
                layout.label_lyrics.setToolTip(track.get_lyrics_original())
                layout.state_indicator.set_state(State.TAGS_READ)
                layout.state_indicator.setToolTip(State.TAGS_READ.value)
                layout.state = State.TAGS_READ

    @QtCore.Slot()
    def remove_selected_layouts(self) -> None:
        """Remove the selected layouts."""
        for track, layout_item in self.track_layouts_items.copy().items():
            layout = layout_item[0]
            item = layout_item[1]
            if layout.selected:
                self.remove_layout(track, item)
        self.selection_changed()

    @QtCore.Slot()
    def selection_changed(self) -> None:
        """Selection of the tracks changed.

        Toggles the cancel and remove buttons, and changes lyrics color.
        """
        enable_cancel = False
        enable_remove = False
        for track, layout_item in self.track_layouts_items.items():
            layout = layout_item[0]
            if layout.selected:
                enable_remove = True
                if track.has_lyrics_new():
                    enable_cancel = True
        self.action_cancel_rows.setEnabled(enable_cancel)
        self.action_remove_rows.setEnabled(enable_remove)

    @QtCore.Slot()
    def lyrics_changed(self) -> None:
        """Lyrics of a track changed."""
        enable_save = False
        for track, layout_item in self.track_layouts_items.items():
            layout = layout_item[0]
            if track.has_lyrics_new():
                # Track has new lyrics
                enable_save = True
                layout.label_lyrics.setStyleSheet(
                    f"color: {CustomColors.LIGHT_GREEN.value}"
                )
            else:
                layout.label_lyrics.setStyleSheet("")
        self.action_save_lyrics.setEnabled(enable_save)
        self.selection_changed()  # Update the cancel and remove buttons

    @QtCore.Slot()
    def filter_tracks(self) -> None:
        """Apply the filters to the track layouts."""
        show_lyrics = self.button_filter_lyrics.isChecked()
        match_case = self.button_filter_case.isChecked()
        text = self.input_filter_text.text()
        if not match_case:
            text = text.casefold()

        # Apply the filters
        for track, layout_items in self.track_layouts_items.items():
            item = layout_items[1]
            visible = False
            if show_lyrics or not track.has_lyrics_original():
                if not match_case:
                    title = track.get_title().casefold()
                    artists = track.get_artists().casefold()
                else:
                    title = track.get_title()
                    artists = track.get_artists()
                if text in title or text in artists:
                    visible = True
            item.setHidden(not visible)

        # Update the lyrics filter button
        if show_lyrics:
            self.button_filter_lyrics.setToolTip("Hide files with lyrics")
        else:
            self.button_filter_lyrics.setToolTip("Show files with lyrics")

    @QtCore.Slot()
    def sort_tracks(self) -> None:
        """Sort the tracks based on their title."""
        if self.sort == Sort.ASCENDING:
            self.sort = Sort.DESCENDING
            self.button_sort_title.setIcon(self.icon_sort_title_descending)
            self.list_tracks.sortItems(QtCore.Qt.SortOrder.DescendingOrder)
        elif self.sort == Sort.DESCENDING:
            self.sort = Sort.ASCENDING
            self.button_sort_title.setIcon(self.icon_sort_title_ascending)
            self.list_tracks.sortItems(QtCore.Qt.SortOrder.AscendingOrder)

    @QtCore.Slot()
    def stop_search(self) -> None:
        """Stop searching for the lyrics."""
        if self.thread_search_lyrics.isRunning():
            self.thread_search_lyrics.stop_search = True
            self.button_stop_search.setEnabled(False)

    @QtCore.Slot()
    def lyrics_searched(self) -> None:
        """Lyrics of a track searched."""
        self.increment_progression_bar()

    @QtCore.Slot()
    def open_token_page(self) -> None:
        """Open the Genius website to fetch the client access token."""
        QtGui.QDesktopServices.openUrl(URL_TOKEN)

    @QtCore.Slot()
    def open_settings(self) -> None:
        """Open the settings window."""
        self.window_settings.show()

    @QtCore.Slot()
    def open_information(self) -> None:
        """Open the information window."""
        self.window_information.show()

    @QtCore.Slot()
    def open_help(self) -> None:
        """Open the help window."""
        self.window_help.show()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        """Intercept the key press event of the main windows.

        Detects the following key events:
        - `Ctrl+A` : Select all tracks.
        - `Ctrl+D` : Deselect all tracks.

        Args:
            event (QtGui.QKeyEvent): Key press event.
        """
        if (
            event.modifiers() == QtCore.Qt.ControlModifier
            and event.key() == QtCore.Qt.Key_A
        ):
            # Selection
            for layout_item in self.track_layouts_items.values():
                track_layout = layout_item[0]
                track_layout.toggle_selection(force=True)
            self.action_cancel_rows.setEnabled(True)
            self.action_remove_rows.setEnabled(True)
        elif (
            event.modifiers() == QtCore.Qt.ControlModifier
            and event.key() == QtCore.Qt.Key_D
        ):
            # Deselection
            for layout_item in self.track_layouts_items.values():
                track_layout = layout_item[0]
                track_layout.toggle_selection(force=False)
            self.action_cancel_rows.setEnabled(False)
            self.action_remove_rows.setEnabled(False)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Intercept the close event of the main window.

        If it is running, waits for `ThreadLyricsSearch` to quit before exiting the application.

        Args:
            event (QtGui.QCloseEvent): Close event.
        """
        if (
            hasattr(self, "thread_search_lyrics")
            and self.thread_search_lyrics.isRunning()
        ):
            self.thread_search_lyrics.stop_search = True
            self.thread_search_lyrics.wait()
        event.accept()
