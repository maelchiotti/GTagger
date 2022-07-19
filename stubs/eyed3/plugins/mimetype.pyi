import eyed3.utils
import magic
from _typeshed import Incomplete
from eyed3.mimetype import guessMimetype as guessMimetype
from eyed3.utils.log import getLogger as getLogger

log: Incomplete

class MagicTypes(magic.Magic):
    def __init__(self) -> None: ...
    def guess_type(self, filename, all_types: bool = ...): ...

class MimetypesPlugin(eyed3.plugins.LoaderPlugin):
    NAMES: Incomplete
    magic: Incomplete
    start_t: Incomplete
    mime_types: Incomplete
    def __init__(self, arg_parser) -> None: ...
    def start(self, args, config) -> None: ...
    def handleFile(self, f, *args, **kwargs) -> None: ...
    def handleDone(self) -> None: ...
