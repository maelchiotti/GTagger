"""Icons."""
import os
import sys
from typing import Optional

from PySide6 import QtGui
from qtawesome import icon as qtawesome_icon


def get_icon(
    name: str,
    active: Optional[str] = None,
    color: str = "white",
    color_active: str = "white",
) -> QtGui.QIcon:
    """Return the MDI6 icon `name` as a `QIcon`.

    Args:
        name (str): Name of the MDI6 icon.
        active (Optional[str]): Name of the MDI6 icon when the button is active. Defaults to None.
        color (str): Color of the icon. Defaults to "white".
        color_active (str): Color of the icon when the button is active. Defaults to "white".

    Returns:
        QtGui.QIcon: MDI6 icon `name` as a `QIcon`.
    """
    name = f"mdi6.{name}"
    if active is None:
        active = name
    return qtawesome_icon(name, active=active, color=color, color_active=color_active)


def get_resource_path(relative_path: str):
    """Return the absolute path to the resource.

    Args:
        relative_path (str): Relative path to the resource.

    Returns:
        str: Absolute path to the resource.
    """

    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
