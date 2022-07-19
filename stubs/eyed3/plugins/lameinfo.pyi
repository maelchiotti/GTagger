from _typeshed import Incomplete
from eyed3.plugins import LoaderPlugin as LoaderPlugin
from eyed3.utils import formatSize as formatSize
from eyed3.utils.console import getTtySize as getTtySize, printMsg as printMsg

class LameInfoPlugin(LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    DESCRIPTION: str
    def printHeader(self, file_path) -> None: ...
    def handleFile(self, f, *_, **__) -> None: ...
