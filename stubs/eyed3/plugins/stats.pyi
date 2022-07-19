from _typeshed import Incomplete
from collections import Counter
from eyed3 import id3 as id3, mp3 as mp3
from eyed3.core import AUDIO_MP3 as AUDIO_MP3
from eyed3.id3 import frames as frames
from eyed3.mimetype import guessMimetype as guessMimetype
from eyed3.plugins import LoaderPlugin as LoaderPlugin
from eyed3.utils.console import Fore as Fore, Style as Style, printMsg as printMsg

ID3_VERSIONS: Incomplete

class Rule:
    def test(self, path, audio_file) -> None: ...

PREFERRED_ID3_VERSIONS: Incomplete

class Id3TagRules(Rule):
    def test(self, path, audio_file): ...

class BitrateRule(Rule):
    BITRATE_DEDUCTIONS: Incomplete
    def test(self, path, audio_file): ...

VALID_MIME_TYPES: Incomplete

class FileRule(Rule):
    def test(self, path, audio_file): ...

VALID_ARTWORK_NAMES: Incomplete

class ArtworkRule(Rule):
    def test(self, path, audio_file): ...

BAD_FRAMES: Incomplete

class Id3FrameRules(Rule):
    def test(self, path, audio_file): ...

class Stat(Counter):
    TOTAL: str
    def __init__(self, *args, **kwargs) -> None: ...
    def compute(self, file, audio_file) -> None: ...
    def report(self) -> None: ...
    def percent(self, key): ...

class AudioStat(Stat):
    def compute(self, audio_file) -> None: ...

class FileCounterStat(Stat):
    SUPPORTED_AUDIO: str
    UNSUPPORTED_AUDIO: str
    HIDDEN_FILES: str
    OTHER_FILES: str
    def __init__(self) -> None: ...

class MimeTypeStat(Stat): ...

class Id3VersionCounter(AudioStat):
    def __init__(self) -> None: ...

class Id3FrameCounter(AudioStat): ...

class BitrateCounter(AudioStat):
    bitrate_keys: Incomplete
    def __init__(self) -> None: ...

class RuleViolationStat(Stat): ...

class Id3ImageTypeCounter(AudioStat):
    def __init__(self) -> None: ...

class StatisticsPlugin(LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    def __init__(self, arg_parser) -> None: ...
    def handleFile(self, path) -> None: ...
    def handleDone(self): ...
