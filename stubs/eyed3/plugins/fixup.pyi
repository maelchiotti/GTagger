from _typeshed import Incomplete
from eyed3 import core as core
from eyed3.core import ALBUM_TYPE_IDS as ALBUM_TYPE_IDS, COMP_TYPE as COMP_TYPE, DEMO_TYPE as DEMO_TYPE, EP_MAX_SIZE_HINT as EP_MAX_SIZE_HINT, EP_TYPE as EP_TYPE, LIVE_TYPE as LIVE_TYPE, LP_TYPE as LP_TYPE, SINGLE_TYPE as SINGLE_TYPE, TXXX_ALBUM_TYPE as TXXX_ALBUM_TYPE, VARIOUS_ARTISTS as VARIOUS_ARTISTS, VARIOUS_TYPE as VARIOUS_TYPE
from eyed3.id3 import ID3_V2_4 as ID3_V2_4
from eyed3.id3.tag import TagTemplate as TagTemplate
from eyed3.plugins import LoaderPlugin as LoaderPlugin
from eyed3.utils import art as art
from eyed3.utils.console import Fore as Fore, Style as Style, printMsg as printMsg
from eyed3.utils.prompt import prompt as prompt

NORMAL_FNAME_FORMAT: str
VARIOUS_FNAME_FORMAT: str
SINGLE_FNAME_FORMAT: str
NORMAL_DNAME_FORMAT: str
LIVE_DNAME_FORMAT: str

def dirDate(d): ...

class FixupPlugin(LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    DESCRIPTION: Incomplete
    def __init__(self, arg_parser) -> None: ...
    def start(self, args, config) -> None: ...
    def handleFile(self, f, *args, **kwargs) -> None: ...
    def handleDirectory(self, directory, _): ...
    def handleDone(self) -> None: ...

ARGS_HELP: Incomplete
