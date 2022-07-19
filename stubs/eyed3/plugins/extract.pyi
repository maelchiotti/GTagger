import eyed3.plugins
from _typeshed import Incomplete
from eyed3.utils.log import getLogger as getLogger

log: Incomplete

class ExtractPlugin(eyed3.plugins.LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    def __init__(self, arg_parser) -> None: ...
    def handleFile(self, f, *args, **kwargs): ...
