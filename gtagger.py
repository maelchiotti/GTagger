"""Runs GTagger."""

import sys

import qdarktheme
from PySide6 import QtCore, QtWidgets

from src.utils import Color_, Mode, Settings, SettingsManager
from src.window_main import WindowMain


class GTagger(QtWidgets.QApplication):
    """GTagger application.

    Attributes:
        settings_manager (SettingsManager): Settings manager of the application.
        mode (Mode): Current layout mode of the application.
    """

    def __init__(self) -> None:
        super().__init__()

        QtCore.QCoreApplication.setOrganizationName("Maël Chiotti")
        QtCore.QCoreApplication.setApplicationName("GTagger")
        QtCore.QCoreApplication.setOrganizationDomain("https://github.com/maelchiotti")

        # Create the settings manager
        self.settings_manager: SettingsManager = SettingsManager()

        # Set the application stylsheet
        self.set_stylesheet()

        # Load the mode setting and default it to normal if it is not set
        self.mode: Mode = Mode.get_mode(
            self.settings_manager.get_setting(Settings.MODE.value, Mode.NORMAL.value)
        )

    def set_stylesheet(self):
        """Sets the stylesheet of the application.

        Uses the dark stylesheet of `qdarktheme` and adds some custom styling.
        """
        self.setStyleSheet(
            qdarktheme.load_stylesheet("dark", "rounded")
            + """
            
            QCheckBox:unchecked:hover {
                border-bottom: 2px solid """
            + Color_.yellow_genius.value
            + """;
            }
            QCheckBox:checked:hover {
                border-bottom: 2px solid """
            + Color_.yellow_genius.value
            + """;
            }
            
            QProgressBar {
                color: """
            + Color_.grey.value
            + """;
            }
            QProgressBar::chunk {
                background-color: """
            + Color_.yellow_genius.value
            + """;
            }
            """
        )


if __name__ == "__main__":
    gtagger = GTagger()

    main_window = WindowMain(gtagger)
    main_window.resize(1200, 800)
    main_window.show()

    sys.exit(gtagger.exec())
