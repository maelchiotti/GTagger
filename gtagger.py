"""Runs GTagger."""

import sys

import qdarktheme
from PySide6 import QtCore, QtWidgets

from src.consts import SIZE_MAIN_WINDOW
from src.enums import CustomColors
from src.settings import SettingsManager
from src.window_main import WindowMain


class GTagger(QtWidgets.QApplication):
    """GTagger application.

    Attributes:
        settings_manager (SettingsManager): Settings manager of the application.
    """

    def __init__(self) -> None:
        """Init GTagger."""
        super().__init__()

        QtCore.QCoreApplication.setOrganizationName("Maël Chiotti")
        QtCore.QCoreApplication.setApplicationName("GTagger")
        QtCore.QCoreApplication.setOrganizationDomain("https://github.com/maelchiotti")

        # Create the settings manager
        self.settings_manager: SettingsManager = SettingsManager()

        # Set the application stylesheet
        self.set_stylesheet()

    def set_stylesheet(self):
        """Set the stylesheet of the application.

        Use the dark stylesheet of `qdarktheme` and add some custom styling.
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
    main_window.resize(SIZE_MAIN_WINDOW)
    main_window.show()

    sys.exit(gtagger.exec())
