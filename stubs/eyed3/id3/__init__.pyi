from . import frames as frames
from .. import Error, core
from .tag import FileInfo as FileInfo, Tag as Tag, TagException as TagException, TagTemplate as TagTemplate
from _typeshed import Incomplete
from collections.abc import Generator

log: Incomplete
ID3_V1: Incomplete
ID3_V1_0: Incomplete
ID3_V1_1: Incomplete
ID3_V2: Incomplete
ID3_V2_2: Incomplete
ID3_V2_3: Incomplete
ID3_V2_4: Incomplete
ID3_DEFAULT_VERSION = ID3_V2_4
ID3_ANY_VERSION: Incomplete
LATIN1_ENCODING: bytes
UTF_16_ENCODING: bytes
UTF_16BE_ENCODING: bytes
UTF_8_ENCODING: bytes
DEFAULT_LANG: bytes
ID3_MIME_TYPE: str
ID3_MIME_TYPE_EXTENSIONS: Incomplete

def isValidVersion(v, fully_qualified: bool = ...): ...
def normalizeVersion(v): ...
def versionToString(v): ...

class GenreException(Error): ...

class Genre:
    def __init__(self, name: Incomplete | None = ..., id: int = ..., genre_map: Incomplete | None = ...) -> None: ...
    @property
    def id(self): ...
    @id.setter
    def id(self, val) -> None: ...
    @property
    def name(self): ...
    @name.setter
    def name(self, val) -> None: ...
    @staticmethod
    def parse(g_str, id3_std: bool = ...): ...
    def __eq__(self, rhs): ...
    def __lt__(self, rhs): ...

class GenreMap(dict):
    GENRE_MIN: int
    GENRE_MAX: Incomplete
    ID3_GENRE_MIN: int
    ID3_GENRE_MAX: int
    WINAMP_GENRE_MIN: int
    WINAMP_GENRE_MAX: int
    GENRE_ID3V1_MAX: int
    def __init__(self, *args) -> None: ...
    def get(self, key): ...
    def __getitem__(self, key): ...
    @property
    def ids(self): ...
    def iter(self) -> Generator[Incomplete, None, None]: ...

class TagFile(core.AudioFile):
    def __init__(self, path, version=...) -> None: ...
    tag: Incomplete
    def initTag(self, version=...) -> None: ...

ID3_GENRES: Incomplete
genres: Incomplete
