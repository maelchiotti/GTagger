from _typeshed import Incomplete
from eyed3.plugins import LoaderPlugin as LoaderPlugin
from eyed3.utils.console import printMsg as printMsg

class Xep118Plugin(LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    def __init__(self, arg_parser) -> None: ...
    def handleFile(self, f, *args, **kwargs) -> None: ...
    def getXML(self, audio_file): ...
