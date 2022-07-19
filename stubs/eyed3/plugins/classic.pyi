from _typeshed import Incomplete
from eyed3 import core as core, id3 as id3, mp3 as mp3
from eyed3.id3.frames import ImageFrame as ImageFrame
from eyed3.mimetype import guessMimetype as guessMimetype
from eyed3.plugins import LoaderPlugin as LoaderPlugin
from eyed3.utils import b as b, formatTime as formatTime, makeUniqueFileName as makeUniqueFileName
from eyed3.utils.console import boldText as boldText, getTtySize as getTtySize, printError as printError, printMsg as printMsg, printWarning as printWarning
from eyed3.utils.log import getLogger as getLogger

log: Incomplete
FIELD_DELIM: str
DEFAULT_MAX_PADDING: Incomplete

class ClassicPlugin(LoaderPlugin):
    SUMMARY: str
    DESCRIPTION: str
    NAMES: Incomplete
    def __init__(self, arg_parser): ...
    terminal_width: Incomplete
    def handleFile(self, f) -> None: ...
    def printHeader(self, file_path) -> None: ...
    def printAudioInfo(self, info) -> None: ...
    def printTag(self, tag) -> None: ...
    def handleRemoves(self, tag): ...
    def handlePadding(self, tag): ...
    def handleEdits(self, tag): ...

ARGS_HELP: Incomplete
