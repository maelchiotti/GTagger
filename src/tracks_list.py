"""List of the tracks."""

from __future__ import annotations

from pathlib import Path

from PySide6 import QtCore, QtWidgets


class CustomListWidget(QtWidgets.QListWidget):
    """Custom implementation of a `QListWidget` accepting files and directories drop events.

    Signals:
        dropped_elements (list): Elements (files or directories) were dropped.
    """

    dropped_elements = QtCore.Signal(list)

    def __init__(self):
        """Init CustomListWidget."""
        super().__init__()

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QtCore.QEvent.Type.DragEnter):
        """Intercept the drag enter event.

        Args:
            event (QtCore.Qt.QEvent.Type.DragEnter): Drag enter event.
        """
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QtCore.QEvent.Type.DragMove):
        """Intercept the drag move event.

        Args:
            event (QtCore.Qt.QEvent.Type.DragMove): Drag move event.
        """
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtCore.QEvent.Type.Drop):
        """Intercept the drop event.

        Args:
            event (QtCore.Qt.QEvent.Type.Drop): Drop event.
        """
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.DropAction.CopyAction)
            event.accept()
            paths = []
            paths.extend(Path(path.toLocalFile()) for path in event.mimeData().urls())
            self.dropped_elements.emit(paths)
        else:
            event.ignore()


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
