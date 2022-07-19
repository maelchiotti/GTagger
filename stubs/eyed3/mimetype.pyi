import filetype
from .id3 import ID3_MIME_TYPE as ID3_MIME_TYPE, ID3_MIME_TYPE_EXTENSIONS as ID3_MIME_TYPE_EXTENSIONS
from .utils.log import getLogger as getLogger
from _typeshed import Incomplete

log: Incomplete

def guessMimetype(filename): ...

class Mp2x(filetype.Type):
    MIME: Incomplete
    EXTENSION: str
    def __init__(self) -> None: ...
    def match(self, buf): ...

class Mp3Invalids(filetype.Type):
    MIME: Incomplete
    EXTENSION: str
    def __init__(self) -> None: ...
    def match(self, buf): ...

class Id3Tag(filetype.Type):
    MIME: Incomplete
    EXTENSION: str
    def __init__(self) -> None: ...
    def match(self, buf): ...

class Id3TagExt(Id3Tag):
    EXTENSION: str

class M3u(filetype.Type):
    MIME: str
    EXTENSION: str
    def __init__(self) -> None: ...
    def match(self, buf): ...
