"""
Application GUI
"""

import sys
import pathlib
from PySide6 import QtCore, QtWidgets, QtGui

import tools

class MainWindow(QtWidgets.QWidget):
    """
    Main window of the GUI
    """
    def __init__(self):
        super().__init__()

        self.tracks = []

        self.input_token = QtWidgets.QLineEdit()
        self.input_token.setPlaceholderText("Enter your Genius client access token")
        self.input_token.setToolTip("Enter token")
        self.input_token.setStyleSheet("border: 0px")
        regex_epx = QtCore.QRegularExpression("[a-zA-Z0-9_-]{64}")
        self.validator = QtGui.QRegularExpressionValidator(regex_epx, self)
        self.input_token.setValidator(self.validator)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["File", "Title", "Main artist", "Lyrics"])

        self.button_add_directories = QtWidgets.QPushButton("Add directory")
        self.button_add_files = QtWidgets.QPushButton("Add files")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.input_token)
        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button_add_directories)
        self.layout.addWidget(self.button_add_files)

        self.input_token.textChanged.connect(self.token_changed)
        self.button_add_directories.clicked.connect(lambda:self.add_files(True))
        self.button_add_files.clicked.connect(lambda:self.add_files(False))

    def select_directories(self) -> str:
        directory_dialog = QtWidgets.QFileDialog()
        directory = directory_dialog.getExistingDirectory()
        if directory == "":
            return None
        return directory

    def select_files(self) -> list[str]:
        file_dialog = QtWidgets.QFileDialog()
        files = file_dialog.getOpenFileNames(caption="Select file(s)", filter="MP3 files (*.mp3)")
        if len(files[0]) == 0:
            return None
        return files[0]

    @QtCore.Slot()
    def add_files(self, select_directory: bool) -> None:
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
            track = tools.Track(file)
            self.tracks.append(track)

            self.table.insertRow(self.table.rowCount())
            self.table.setItem(self.table.rowCount() - 1, 0, QtWidgets.QTableWidgetItem(track.filename))
            self.table.setItem(self.table.rowCount() - 1, 1, QtWidgets.QTableWidgetItem(track.title))
            self.table.setItem(self.table.rowCount() - 1, 2, QtWidgets.QTableWidgetItem(track.main_artist))

            #TODO ce sont juste des tests
            track_search = tools.TrackSearch("8hPJjsOhGDfGB5naUVwKMF7zGK5XCV5-pRsIu55LSQgK_5Yo2HTsBNJnWamF8GMk")
            track_search.search_track(track)
            lyrics_search = tools.LyricsSearch("8hPJjsOhGDfGB5naUVwKMF7zGK5XCV5-pRsIu55LSQgK_5Yo2HTsBNJnWamF8GMk")
            lyrics_search.search_lyrics(track)
            self.table.setItem(self.table.rowCount() - 1, 3, QtWidgets.QTableWidgetItem(track.lyrics[:100]))

    @QtCore.Slot()
    def token_changed(self):
        validator_state = self.validator.validate(self.input_token.text(), 0)[0]
        if len(self.input_token.text()) == 0:
            self.input_token.setStyleSheet("border: 0px")
            self.input_token.setToolTip("Enter token")
        elif validator_state == QtGui.QValidator.State.Acceptable:
            self.input_token.setStyleSheet(f"border: 0px; background-color: {tools.COLORS['light_green']}")
            self.input_token.setToolTip("Valid token")
        else:
            self.input_token.setStyleSheet(f"border: 0px; background-color: {tools.COLORS['light_red']}")
            self.input_token.setToolTip("Invalid token")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())
