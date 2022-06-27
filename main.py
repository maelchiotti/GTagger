"""Runs GTagger."""

import sys
from PySide6 import QtWidgets

from gui import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
