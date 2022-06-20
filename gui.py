"""
Application GUI
"""

import os
import sys
import pathlib
from PySide6 import QtCore, QtWidgets

class MainWindow(QtWidgets.QWidget):
    """
    Main window of the GUI
    """
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["File", "Artist", "Title"])

        self.button_add_directories = QtWidgets.QPushButton("Add directory")
        self.button_add_files = QtWidgets.QPushButton("Add files")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button_add_directories)
        self.layout.addWidget(self.button_add_files)

        self.button_add_directories.clicked.connect(lambda:self.add_files(True))
        self.button_add_files.clicked.connect(lambda:self.add_files(False))

    def select_directories(self):
        directory_dialog = QtWidgets.QFileDialog()
        directory = directory_dialog.getExistingDirectory()
        if directory == "":
            return None
        return directory

    def select_files(self):
        file_dialog = QtWidgets.QFileDialog()
        files = file_dialog.getOpenFileNames(caption="Select file(s)", filter="MP3 files (*.mp3)")
        if len(files[0]) == 0:
            return None
        return files[0]

    @QtCore.Slot()
    def add_files(self, select_directory):
        if select_directory:
            directory = self.select_directories()
            if directory is None:
                return
            files = pathlib.Path(directory).rglob("*.mp3")
        else:
            files = self.select_files()
            if files is None:
                return
        
        for file in files:
            filename = os.path.basename(file)
            item = QtWidgets.QTableWidgetItem(filename)
            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount() - 1, 0, item)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
