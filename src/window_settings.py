"""Application's settings window.

Handles the creation of the settings window and the interactions with the user.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6 import QtCore, QtWidgets

from src.utils import Settings

if TYPE_CHECKING:
    from gtagger import GTagger


class WindowSettings(QtWidgets.QDialog):
    """Settings window of the GUI.

    Args:
        gtagger (GTagger): GTagger application.

    Attributes:
        gtagger (GTagger): GTagger application.
    """

    def __init__(self, parent, gtagger: GTagger):
        super().__init__(parent)

        self.gtagger: GTagger = gtagger

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        self.checkbox_recursive = QtWidgets.QCheckBox("Recursively search for files")
        recursive_search = self.gtagger.settings_manager.get_setting(
            Settings.RECURSIVE_SEARCH.value, default=True, type_=bool
        )
        self.checkbox_recursive.setChecked(recursive_search)

        self.checkbox_overwrite = QtWidgets.QCheckBox(
            "Overwrite already existing lyrics"
        )
        overwrite_lyrics = self.gtagger.settings_manager.get_setting(
            Settings.OVERWRITE_LYRICS.value, default=True, type_=bool
        )
        self.checkbox_overwrite.setChecked(overwrite_lyrics)

        self.grid_files = QtWidgets.QGridLayout()
        self.grid_files.addWidget(self.checkbox_recursive, 0, 0, 1, 1)
        self.grid_files.addWidget(self.checkbox_overwrite, 1, 0, 1, 1)

        self.box_files = QtWidgets.QGroupBox("Files")
        self.box_files.setLayout(self.grid_files)

        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.addWidget(self.box_files, 0, 0, 1, 1)

        self.setLayout(self.layout_)
        self.setWindowTitle("Settings")
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.checkbox_recursive.stateChanged.connect(self.toggle_recursive_search)
        self.checkbox_overwrite.stateChanged.connect(self.toggle_overwrite_lyrics)

    @QtCore.Slot()
    def toggle_recursive_search(self) -> None:
        """Updates the setting for recursively searching for files."""
        recursive_search = self.checkbox_recursive.isChecked()
        self.gtagger.settings_manager.set_setting(
            Settings.RECURSIVE_SEARCH.value, recursive_search
        )

    def toggle_overwrite_lyrics(self) -> None:
        """Updates the setting for overwriting original lyrics."""
        overwrite_lyrics = self.checkbox_overwrite.isChecked()
        self.gtagger.settings_manager.set_setting(
            Settings.OVERWRITE_LYRICS.value, overwrite_lyrics
        )
