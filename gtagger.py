"""Runs GTagger."""

import sys

import qdarktheme
from PySide6 import QtCore, QtWidgets

from src.enums import CustomColors
from src.settings import SettingsManager
from src.window_main import WindowMain
from src.consts import MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT


class GTagger(QtWidgets.QApplication):
    """GTagger application.

    Attributes:
        settings_manager (SettingsManager): Settings manager of the application.
    """

    def __init__(self) -> None:
        super().__init__()

        QtCore.QCoreApplication.setOrganizationName("Maël Chiotti")
        QtCore.QCoreApplication.setApplicationName("GTagger")
        QtCore.QCoreApplication.setOrganizationDomain("https://github.com/maelchiotti")

        # Create the settings manager
        self.settings_manager: SettingsManager = SettingsManager()

        # Set the application stylesheet
        self.set_stylesheet()

    def set_stylesheet(self):
        """Sets the stylesheet of the application.

        Uses the dark stylesheet of `qdarktheme` and adds some custom styling.
        """
        self.setStyleSheet(
            qdarktheme.load_stylesheet("dark", "rounded")
            + """
            
            QCheckBox:unchecked:hover {
                border-bottom: 2px solid """
            + CustomColors.YELLOW_GENIUS.value
            + """;
            }
            QCheckBox:checked:hover {
                border-bottom: 2px solid """
            + CustomColors.YELLOW_GENIUS.value
            + """;
            }
            
            QProgressBar {
                color: """
            + CustomColors.GREY.value
            + """;
            }
            QProgressBar::chunk {
                background-color: """
            + CustomColors.YELLOW_GENIUS.value
            + """;
            }
            """
        )


if __name__ == "__main__":
    gtagger = GTagger()

    main_window = WindowMain(gtagger)
    main_window.resize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
    main_window.show()

    sys.exit(gtagger.exec())
