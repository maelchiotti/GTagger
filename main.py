"""Runs GTagger."""

import sys
import qdarktheme
from PySide6 import QtWidgets

from src.main_window import MainWindow

if __name__ == "__main__":
    gtagger = QtWidgets.QApplication([])
    
    gtagger.setStyleSheet(qdarktheme.load_stylesheet("dark", "rounded"))

    main_window = MainWindow()
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(gtagger.exec())
