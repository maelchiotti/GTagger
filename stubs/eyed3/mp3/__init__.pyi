from .. import Error, core
from _typeshed import Incomplete

log: Incomplete

class Mp3Exception(Error): ...

NAME: str
MIME_TYPES: Incomplete
OTHER_MIME_TYPES: Incomplete
EXTENSIONS: Incomplete

class Mp3AudioInfo(core.AudioInfo):
    mp3_header: Incomplete
    xing_header: Incomplete
    vbri_header: Incomplete
    lame_tag: Incomplete
    bit_rate: Incomplete
    size_bytes: Incomplete
    time_secs: Incomplete
    sample_freq: Incomplete
    mode: Incomplete
    def __init__(self, file_obj, start_offset, tag) -> None: ...
    @property
    def bit_rate_str(self): ...

class Mp3AudioFile(core.AudioFile):
    def __init__(self, path, version=...) -> None: ...
    def initTag(self, version=...): ...
    def tag(self, t) -> None: ...
