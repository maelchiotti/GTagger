"""Runs GTagger."""

import sys
from typing import Any
import qdarktheme
from PySide6 import QtCore, QtWidgets

from src.window_main import WindowMain
from src.tools import Settings, Theme


class GTagger(QtWidgets.QApplication):
    """GTagger application.

    Attributes:
        settings_manager (SettingsManager): Settings manager of the application.
        theme (Theme): Current theme of the application.
    """

    def __init__(self) -> None:
        super().__init__()

        QtCore.QCoreApplication.setOrganizationName("Maël Chiotti")
        QtCore.QCoreApplication.setApplicationName("GTagger")
        QtCore.QCoreApplication.setOrganizationDomain("https://github.com/maelchiotti")

        # Create the settings manager
        self.settings_manager: SettingsManager = SettingsManager()

        # Load the theme setting and default it to dark if it is not set
        setting_theme = self.settings_manager.get_setting(
            Settings.THEME.value, default=Theme.DARK.value
        )
        self.theme: Theme = Theme.get_theme(setting_theme)
        self.setStyleSheet(qdarktheme.load_stylesheet(self.theme.value, "rounded"))


class SettingsManager(QtCore.QObject):
    """Settings manager that handles of the settings of the application.

    Attributes:
        settings (QtCore.QSettings): Settings of the application.
    """

    def __init__(self) -> None:
        super().__init__()

        QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)
        self.settings = QtCore.QSettings()

    def get_setting(
        self, setting: str, default: Any = None, type: object = None
    ) -> object:
        """Returns the value of the setting `setting`.

        The setting is defaulted to `default` if it does not exist,
        which defaults to `None`.

        `type` specifies the type of the data to return,
        it has to be a native data type.

        Args:
            setting (str): Name of the setting.
            default (Any, optional): Default value for the setting. Defaults to `None`.
            type (object, optional): Type of the setting. Defaults to `None`.

        Returns:
            object: Value of the setting.
        """
        if type is None:
            return self.settings.value(setting, defaultValue=default)
        else:
            return self.settings.value(setting, defaultValue=default, type=type)

    def set_setting(self, setting: str, value: object) -> None:
        """Sets the value of `setting` to `value`.

        Args:
            setting (str): Name of the setting.
            value (object): Value of the setting.
        """
        self.settings.setValue(setting, value)


if __name__ == "__main__":
    gtagger = GTagger()

    main_window = WindowMain(gtagger)
    main_window.resize(1200, 800)
    main_window.show()

    sys.exit(gtagger.exec())
