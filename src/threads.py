"""Application's threads.

Threads handle long operations in the background to avoid blocking the GUI.

Includes:
- ThreadSearchLyrics: search tracks' lyrics.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6 import QtCore, QtGui

from src.track_search import TrackSearch
from src.lyrics_search import LyricsSearch
from src.tools import State

if TYPE_CHECKING:
    from main_window import MainWindow


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
                lyrics = f"{track.get_lyrics(lines=5)}[...]"
                item = QtGui.QStandardItem(lyrics)
                item.setToolTip(track.lyrics)
                self.main.table_model.setItem(row, 3, item)
                self.main.table_model.setItem(
                    row, 4, QtGui.QStandardItem(State.LYRICS_FOUND.value)
                )
            else:
                self.main.table_model.setItem(
                    row, 4, QtGui.QStandardItem(State.LYRICS_NOT_FOUND.value)
                )
