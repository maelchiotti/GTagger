from _typeshed import Incomplete
from eyed3.id3 import versionToString as versionToString
from eyed3.plugins import LoaderPlugin as LoaderPlugin
from eyed3.utils import formatSize as formatSize, formatTime as formatTime
from eyed3.utils.console import printMsg as printMsg

class NfoPlugin(LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    DESCRIPTION: str
    albums: Incomplete
    def __init__(self, arg_parser) -> None: ...
    def handleFile(self, f) -> None: ...
    def handleDone(self): ...
