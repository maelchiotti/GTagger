"""List of the tracks."""

from __future__ import annotations

from PySide6 import QtWidgets


class CustomListWidgetItem(QtWidgets.QListWidgetItem):
    """Custom implementation of a `QListWidgetItem` containing the title of the track.

    Attributes:
        title (str): Title of the track used for comparison.
    """

    def __init__(self, title: str, listview: QtWidgets.QListWidget | None = ...):
        """Init CustomListWidgetItem.

        Args:
            title (str): Title of the track used for comparison.
            listview (QtWidgets.QListWidget | None): `QListWidget` to pass to the parent class.
        """
        super().__init__(listview)
        self.title: str = title

    def __lt__(self, other: CustomListWidgetItem) -> bool:
        """Return `True` if the title of this item is lower than the `other`'s one.

        Args:
            other (CustomListWidgetItem): Other item on which to perform the comparison.

        Returns:
            bool: `True` if the title of this item is lower than the `other`'s one.
        """
        try:
            return self.title < other.title
        except AttributeError:
            return False
