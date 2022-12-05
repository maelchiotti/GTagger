"""Icons."""

from typing import Optional

from PySide6 import QtGui
from qtawesome import icon as qtawesome_icon


def get_icon(
    name: str,
    active: Optional[str] = None,
    color: str = "white",
    color_active: str = "white",
) -> QtGui.QIcon:
    """Returns the MDI6 icon `name` as a `QIcon`.

    Args:
        name (str): Name of the MDI6 icon.
        active (str, optional): Name of the MDI6 icon when the button is active. Defaults to None.
        color (str, optional): Color of the icon. Defaults to "white".
        color_active (str, optional): Color of the icon when the button is active. Defaults to "white".

    Returns:
        QtGui.QIcon: MDI6 icon `name` as a `QIcon`.
    """
    name = f"mdi6.{name}"
    if active is None:
        active = name
    return qtawesome_icon(name, active=active, color=color, color_active=color_active)
