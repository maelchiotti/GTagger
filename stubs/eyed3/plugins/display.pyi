import abc
from _typeshed import Incomplete
from eyed3 import id3 as id3
from eyed3.plugins import LoaderPlugin as LoaderPlugin
from eyed3.plugins._display_parser import DisplayPatternParser as DisplayPatternParser
from eyed3.utils import console as console, formatSize as formatSize, formatTime as formatTime

class Pattern:
    def __init__(self, text: Incomplete | None = ..., sub_patterns: Incomplete | None = ...) -> None: ...
    def output_for(self, audio_file): ...
    sub_patterns: Incomplete
    @staticmethod
    def sub_pattern_classes(base_class): ...
    @staticmethod
    def pattern_class_parameters(pattern_class): ...

class TextPattern(Pattern):
    SPECIAL_CHARACTERS: Incomplete
    SPECIAL_CHARACTERS_DESCRIPTIONS: Incomplete
    def __init__(self, text) -> None: ...
    def output_for(self, audio_file): ...

class ComplexPattern(Pattern, metaclass=abc.ABCMeta):
    __metaclass__: Incomplete
    TYPE: str
    NAMES: Incomplete
    DESCRIPTION: str
    PARAMETERS: Incomplete
    class ExpectedParameter:
        name: Incomplete
        requried: bool
        default: Incomplete
        def __init__(self, name, **kwargs) -> None: ...
    class Parameter:
        value: Incomplete
        provided: Incomplete
        def __init__(self, value, provided) -> None: ...
    def __init__(self, name, parameters) -> None: ...
    def output_for(self, audio_file): ...
    parameters: Incomplete
    name: Incomplete

class PlaceholderUsagePattern:
    __metaclass__: Incomplete

class TagPattern(ComplexPattern, metaclass=abc.ABCMeta):
    __metaclass__: Incomplete
    TYPE: str

class ArtistTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class AlbumTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class AlbumArtistTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class ComposerTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class TitleTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class TrackTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class TrackTotalTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class DiscTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class DiscTotalTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class GenreTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class GenreIdTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class YearTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class DescriptableTagPattern(TagPattern, metaclass=abc.ABCMeta):
    __metaclass__: Incomplete
    PARAMETERS: Incomplete

class CommentTagPattern(DescriptableTagPattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class AllCommentsTagPattern(DescriptableTagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class AbstractDateTagPattern(TagPattern, metaclass=abc.ABCMeta):
    __metaclass__: Incomplete

class ReleaseDateTagPattern(AbstractDateTagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class OriginalReleaseDateTagPattern(AbstractDateTagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class RecordingDateTagPattern(AbstractDateTagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class EncodingDateTagPattern(AbstractDateTagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class TaggingDateTagPattern(AbstractDateTagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class PlayCountTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class PopularitiesTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class BPMTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class PublisherTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class UniqueFileIDTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class LyricsTagPattern(DescriptableTagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: Incomplete

class TextsTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class ArtistURLTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class AudioSourceURLTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class AudioFileURLTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class InternetRadioURLTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class CommercialURLTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class PaymentURLTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class PublisherURLTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class CopyrightTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class UserURLsTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class ImagesTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class ImageURLsTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class ObjectsTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class PrivatesTagPattern(TagPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class MusicCDIdTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class TermsOfUseTagPattern(TagPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class FunctionPattern(ComplexPattern, metaclass=abc.ABCMeta):
    __metaclass__: Incomplete
    TYPE: str

class FunctionFormatPattern(FunctionPattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class FunctionNumberPattern(FunctionPattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class FunctionFilenamePattern(FunctionPattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class FunctionFilesizePattern(FunctionPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class FunctionTagVersionPattern(FunctionPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class FunctionLengthPattern(FunctionPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class FunctionMPEGVersionPattern(FunctionPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class FunctionBitRatePattern(FunctionPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class FunctionSampleFrequencePattern(FunctionPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class FunctionAudioModePattern(FunctionPattern):
    NAMES: Incomplete
    DESCRIPTION: str

class FunctionNotEmptyPattern(FunctionPattern, PlaceholderUsagePattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class FunctionRepeatPattern(FunctionPattern):
    NAMES: Incomplete
    PARAMETERS: Incomplete
    DESCRIPTION: str

class DisplayPlugin(LoaderPlugin):
    NAMES: Incomplete
    SUMMARY: str
    DESCRIPTION: str
    def __init__(self, arg_parser): ...
    def start(self, args, config) -> None: ...
    def handleFile(self, f, *args, **kwargs) -> None: ...
    def handleDone(self): ...

class DisplayException(Exception):
    def __init__(self, message) -> None: ...
    message: Incomplete

class PatternCompileException(Exception):
    def __init__(self, message) -> None: ...
    message: Incomplete

ARGS_HELP: Incomplete
