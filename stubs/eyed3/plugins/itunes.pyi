from _typeshed import Incomplete
from eyed3.id3.apple import PCST as PCST, PCST_FID as PCST_FID, WFED as WFED, WFED_FID as WFED_FID
from eyed3.plugins import LoaderPlugin as LoaderPlugin

class Podcast(LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    def __init__(self, arg_parser) -> None: ...
    def handleFile(self, f) -> None: ...
