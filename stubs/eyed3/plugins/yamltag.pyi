import eyed3.plugins
from _typeshed import Incomplete
from eyed3 import log as log
from eyed3.plugins.jsontag import audioFileToJson as audioFileToJson

class YamlTagPlugin(eyed3.plugins.LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    def __init__(self, arg_parser) -> None: ...
    def handleFile(self, f, *args, **kwargs) -> None: ...
