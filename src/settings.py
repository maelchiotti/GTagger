"""Settings."""

from typing import Any, Optional

from PySide6 import QtCore


class SettingsManager(QtCore.QObject):
    """Settings manager that handles the settings of the application.

    Attributes:
        settings (QtCore.QSettings): Settings of the application.
    """

    def __init__(self) -> None:
        """Init SettingsManager."""
        super().__init__()

        QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)
        self.settings = QtCore.QSettings()

    def get_setting(
            self,
            setting: str,
            default: Optional[Any] = None,
            type_: Optional[object] = None,
    ) -> Any:
        """Return the value of the setting `setting`.

        The setting is defaulted to `default` if it does not exist,
        which defaults to `None`.

        `type` specifies the type of the data to return,
        it has to be a native data type.

        Args:
            setting (str): Name of the setting.
            default (Any, optional): Default value for the setting. Defaults to `None`.
            type_ (object, optional): Type of the setting. Defaults to `None`.

        Returns:
            Any: Value of the setting.
        """
        if type_ is None:
            return self.settings.value(setting, defaultValue=default)
        return self.settings.value(setting, defaultValue=default, type=type_)

    def set_setting(self, setting: str, value: object) -> None:
        """Set the value of `setting` to `value`.

        Args:
            setting (str): Name of the setting.
            value (object): Value of the setting.
        """
        self.settings.setValue(setting, value)
