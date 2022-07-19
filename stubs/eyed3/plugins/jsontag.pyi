import eyed3.id3.headers
from _typeshed import Incomplete
from eyed3.utils.log import getLogger as getLogger

log: Incomplete

class JsonTagPlugin(eyed3.plugins.LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    def __init__(self, arg_parser) -> None: ...
    def handleFile(self, f, *args, **kwargs) -> None: ...

def audioFileToJson(audio_file): ...
