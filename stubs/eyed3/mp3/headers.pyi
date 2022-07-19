from . import Mp3Exception as Mp3Exception
from ..utils.binfuncs import bin2dec as bin2dec, bytes2bin as bytes2bin, bytes2dec as bytes2dec
from ..utils.log import getLogger as getLogger
from _typeshed import Incomplete

log: Incomplete

def isValidHeader(header): ...
def findHeader(fp, start_pos: int = ...): ...
def timePerFrame(mp3_header, vbr): ...
def compute_time_per_frame(mp3_header): ...

class Mp3Header:
    version: Incomplete
    layer: Incomplete
    error_protection: Incomplete
    bit_rate: Incomplete
    sample_freq: Incomplete
    padding: Incomplete
    private_bit: Incomplete
    copyright: Incomplete
    original: Incomplete
    emphasis: Incomplete
    mode: Incomplete
    mode_extension: Incomplete
    frame_length: Incomplete
    def __init__(self, header_data: Incomplete | None = ...) -> None: ...
    def decode(self, header) -> None: ...

class VbriHeader:
    vbr: bool
    version: Incomplete
    def __init__(self) -> None: ...
    delay: Incomplete
    quality: Incomplete
    num_bytes: Incomplete
    num_frames: Incomplete
    def decode(self, frame): ...

class XingHeader:
    numFrames: Incomplete
    numBytes: Incomplete
    toc: Incomplete
    vbrScale: Incomplete
    def __init__(self) -> None: ...
    vbr: Incomplete
    def decode(self, frame): ...

class LameHeader(dict):
    ENCODER_FLAGS: Incomplete
    PRESETS: Incomplete
    REPLAYGAIN_NAME: Incomplete
    REPLAYGAIN_ORIGINATOR: Incomplete
    SAMPLE_FREQUENCIES: Incomplete
    STEREO_MODES: Incomplete
    SURROUND_INFO: Incomplete
    VBR_METHODS: Incomplete
    def __init__(self, frame) -> None: ...
    def decode(self, frame) -> None: ...

def lamevercmp(x, y): ...

SAMPLE_FREQ_TABLE: Incomplete
BIT_RATE_TABLE: Incomplete
SAMPLES_PER_FRAME_TABLE: Incomplete
EMPHASIS_NONE: str
EMPHASIS_5015: str
EMPHASIS_CCIT: str
MODE_STEREO: str
MODE_JOINT_STEREO: str
MODE_DUAL_CHANNEL_STEREO: str
MODE_MONO: str
FRAMES_FLAG: int
BYTES_FLAG: int
TOC_FLAG: int
VBR_SCALE_FLAG: int
