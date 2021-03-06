"""Application's settings window.

Handles the creation of the settings window and the interactions with the user.
"""

from typing import Any
from PySide6 import QtCore, QtWidgets


class SettingsWindow(QtWidgets.QWidget):
    """Settings window of the GUI.

    Attributes:
        ui_window (QtWidgets.QMainWindow): Main window UI.
        settings (dict[str, Any]): Settings names and values.
    """

    def __init__(self, parent, ui_window: QtWidgets.QMainWindow):
        super().__init__(parent)

        self.ui_window: QtWidgets.QMainWindow = ui_window
        self.settings: dict[str, Any] = {
            "recursive": True,
        }

        self.setup_ui()

    def setup_ui(self) -> None:
        """Sets up the UI of the window."""
        self.checkbox_recursive = QtWidgets.QCheckBox("Recursively search for files")
        self.checkbox_recursive.setChecked(True)

        self.grid_files = QtWidgets.QGridLayout()
        self.grid_files.addWidget(self.checkbox_recursive, 0, 0, 1, 1)

        self.box_files = QtWidgets.QGroupBox("Files")
        self.box_files.setLayout(self.grid_files)

        self.centralwidget = QtWidgets.QWidget(self.ui_window)
        self.layout = QtWidgets.QGridLayout(self.centralwidget)
        self.ui_window.setCentralWidget(self.centralwidget)

        self.layout.addWidget(self.box_files, 0, 0, 1, 1)

        self.ui_window.setWindowTitle("Settings")

        self.checkbox_recursive.stateChanged.connect(self.recursive)

    def get_setting(self, setting: str) -> Any:
        """Returns the current value for `setting`.

        Args:
            setting (str): Name of the setting.

        Returns:
            Any: The value of the setting.
        """
        if setting in self.settings:
            return self.settings[setting]
        else:
            return None

    @QtCore.Slot()
    def recursive(self) -> None:
        """Updates the setting for resursively searching for files."""
        self.settings["recursive"] = self.checkbox_recursive.isChecked()
