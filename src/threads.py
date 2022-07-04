"""Application's threads.

Threads handle long operations in the background to avoid blocking the GUI.
The threads include:
- ThreadAddRows: add rows to the main table.
- ThreadSearchLyrics: search tracks' lyrics.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6 import QtCore, QtGui, QtWidgets

from src.track import Track
from src.track_search import TrackSearch
from src.lyrics_search import LyricsSearch
from src.tools import States

if TYPE_CHECKING:
    from main_window import MainWindow


class ThreadAddRows(QtCore.QThread):
    """Runs the thread for `main.add_files()`.

    Attributes:
        main (MainWindow): Main window.
        files (list[str]): List of files to add to the table.
    """
    added_row = QtCore.Signal(object)

    def __init__(self, main: MainWindow, files: list[str]):
        super().__init__()

        self.main: MainWindow = main
        self.files: list[str] = files

    def run(self):
        for file in self.files:
            track = Track(file)
            tags_read = track.read_tags()
            self.main.tracks[track.filename] = track

            item_filename = QtGui.QStandardItem(track.filename)
            item_filename.setToolTip(str(track.filepath))
            
            if tags_read:
                label_filename = QtWidgets.QLabel()
                label_title = QtWidgets.QLabel()
                label_artist = QtWidgets.QLabel()
                label_lyrics = QtWidgets.QLabel()
                label_state = QtWidgets.QLabel()
            else:
                label_filename = QtWidgets.QLabel("")
                label_title = QtWidgets.QLabel("")
                label_artist = QtWidgets.QLabel("")
                label_lyrics = QtWidgets.QLabel("")
                label_state = QtWidgets.QLabel(States.TAGS_NOT_READ.value)
            
            layout = QtWidgets.QGridLayout()
            layout.addWidget(label_filename, 0, 0, 1, 2)
            layout.addWidget(label_title, 1, 0, 1, 1)
            layout.addWidget(label_artist, 1, 1, 1, 1)
            layout.addWidget(label_lyrics, 2, 0, 1, 2)
            layout.addWidget(label_state, 3, 0, 1, 2)
        
            print("built")
            self.added_row.emit(layout)

        if self.main.is_token_valid():
            self.main.action_search_lyrics.setEnabled(True)


class ThreadSearchLyrics(QtCore.QThread):
    """Runs the thread for `main.search_lyrics()`.

    Attributes:
        main (MainWindow): Main window.
    """

    def __init__(self, main: MainWindow) -> None:
        super().__init__()

        self.main: MainWindow = main

    def run(self):
        if (
            self.main.table_model.rowCount() == 0
            or self.main.thread_add_rows is None
            or self.main.thread_add_rows.isRunning()
        ):
            return

        token = self.main.input_token.text()
        for row, track in enumerate(self.main.tracks.values()):
            track_search = TrackSearch(token)
            track_search.search_track(track)
            lyrics_search = LyricsSearch(token)
            found_lyrics = lyrics_search.search_lyrics(track)
            if found_lyrics:
                lyrics = f"{track.get_lyrics(100)}[...]"
                item = QtGui.QStandardItem(lyrics)
                item.setToolTip(track.lyrics)
                self.main.table_model.setItem(row, 3, item)
                self.main.table_model.setItem(
                    row, 4, QtGui.QStandardItem(States.LYRICS_FOUND.value)
                )
            else:
                self.main.table_model.setItem(
                    row, 4, QtGui.QStandardItem(States.LYRICS_NOT_FOUND.value)
                )
