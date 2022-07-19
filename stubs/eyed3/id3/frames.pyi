from . import DEFAULT_LANG as DEFAULT_LANG, ID3_V2 as ID3_V2, ID3_V2_2 as ID3_V2_2, ID3_V2_3 as ID3_V2_3, ID3_V2_4 as ID3_V2_4, LATIN1_ENCODING as LATIN1_ENCODING, UTF_16BE_ENCODING as UTF_16BE_ENCODING, UTF_16_ENCODING as UTF_16_ENCODING, UTF_8_ENCODING as UTF_8_ENCODING, apple as apple
from .. import Error as Error, core as core
from ..utils import b as b, requireBytes as requireBytes, requireUnicode as requireUnicode
from ..utils.binfuncs import bin2bytes as bin2bytes, bin2dec as bin2dec, bytes2bin as bytes2bin, bytes2dec as bytes2dec, bytes2signedInt16 as bytes2signedInt16, dec2bin as dec2bin, dec2bytes as dec2bytes, signedInt162bytes as signedInt162bytes
from ..utils.log import getLogger as getLogger
from .headers import FrameHeader as FrameHeader
from _typeshed import Incomplete
from typing import NamedTuple

log: Incomplete
ISO_8859_1: str

class FrameException(Error): ...

TITLE_FID: bytes
SUBTITLE_FID: bytes
ARTIST_FID: bytes
ALBUM_ARTIST_FID: bytes
ORIG_ARTIST_FID: bytes
COMPOSER_FID: bytes
ALBUM_FID: bytes
TRACKNUM_FID: bytes
GENRE_FID: bytes
COMMENT_FID: bytes
USERTEXT_FID: bytes
OBJECT_FID: bytes
UNIQUE_FILE_ID_FID: bytes
LYRICS_FID: bytes
DISCNUM_FID: bytes
IMAGE_FID: bytes
USERURL_FID: bytes
PLAYCOUNT_FID: bytes
BPM_FID: bytes
PUBLISHER_FID: bytes
CDID_FID: bytes
PRIVATE_FID: bytes
TOS_FID: bytes
POPULARITY_FID: bytes
ENCODED_BY_FID: bytes
COPYRIGHT_FID: bytes
URL_COMMERCIAL_FID: bytes
URL_COPYRIGHT_FID: bytes
URL_AUDIOFILE_FID: bytes
URL_ARTIST_FID: bytes
URL_AUDIOSRC_FID: bytes
URL_INET_RADIO_FID: bytes
URL_PAYMENT_FID: bytes
URL_PUBLISHER_FID: bytes
URL_FIDS: Incomplete
TOC_FID: bytes
CHAPTER_FID: bytes
DEPRECATED_DATE_FIDS: Incomplete
DATE_FIDS: Incomplete

class Frame:
    id: Incomplete
    decompressed_size: int
    group_id: Incomplete
    encrypt_method: Incomplete
    data: Incomplete
    data_len: int
    def __init__(self, id) -> None: ...
    @property
    def header(self): ...
    @header.setter
    def header(self, h) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    def render(self): ...
    def __lt__(self, other): ...
    @staticmethod
    def decompress(data): ...
    @staticmethod
    def compress(data): ...
    @staticmethod
    def decrypt(data): ...
    @staticmethod
    def encrypt(data): ...
    @property
    def text_delim(self): ...
    @property
    def encoding(self): ...
    @encoding.setter
    def encoding(self, enc) -> None: ...

class TextFrame(Frame):
    def __init__(self, id, text: Incomplete | None = ...) -> None: ...
    @property
    def text(self): ...
    @text.setter
    def text(self, txt) -> None: ...
    encoding: Incomplete
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class UserTextFrame(TextFrame):
    def __init__(self, id=..., description: str = ..., text: str = ...) -> None: ...
    @property
    def description(self): ...
    @description.setter
    def description(self, txt) -> None: ...
    encoding: Incomplete
    text: Incomplete
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class DateFrame(TextFrame):
    encoding: Incomplete
    def __init__(self, id, date: str = ...) -> None: ...
    text: str
    def parse(self, data, frame_header) -> None: ...
    @property
    def date(self): ...
    @date.setter
    def date(self, date) -> None: ...

class UrlFrame(Frame):
    encoding: Incomplete
    def __init__(self, id, url: str = ...) -> None: ...
    @property
    def url(self): ...
    @url.setter
    def url(self, url) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class UserUrlFrame(UrlFrame):
    def __init__(self, id=..., description: str = ..., url: str = ...) -> None: ...
    @property
    def description(self): ...
    @description.setter
    def description(self, desc) -> None: ...
    encoding: Incomplete
    url: Incomplete
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class ImageFrame(Frame):
    OTHER: int
    ICON: int
    OTHER_ICON: int
    FRONT_COVER: int
    BACK_COVER: int
    LEAFLET: int
    MEDIA: int
    LEAD_ARTIST: int
    ARTIST: int
    CONDUCTOR: int
    BAND: int
    COMPOSER: int
    LYRICIST: int
    RECORDING_LOCATION: int
    DURING_RECORDING: int
    DURING_PERFORMANCE: int
    VIDEO: int
    BRIGHT_COLORED_FISH: int
    ILLUSTRATION: int
    BAND_LOGO: int
    PUBLISHER_LOGO: int
    MIN_TYPE: Incomplete
    MAX_TYPE: Incomplete
    URL_MIME_TYPE: bytes
    URL_MIME_TYPE_STR: str
    URL_MIME_TYPE_VALUES: Incomplete
    image_data: Incomplete
    image_url: Incomplete
    def __init__(self, id=..., description: str = ..., image_data: Incomplete | None = ..., image_url: Incomplete | None = ..., picture_type: Incomplete | None = ..., mime_type: Incomplete | None = ...) -> None: ...
    @property
    def description(self): ...
    @description.setter
    def description(self, d) -> None: ...
    @property
    def mime_type(self): ...
    @mime_type.setter
    def mime_type(self, m) -> None: ...
    @property
    def picture_type(self): ...
    @picture_type.setter
    def picture_type(self, t) -> None: ...
    encoding: Incomplete
    desciption: str
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...
    @staticmethod
    def picTypeToString(t): ...
    @staticmethod
    def stringToPicType(s): ...
    def makeFileName(self, name: Incomplete | None = ...): ...

class ObjectFrame(Frame):
    object_data: Incomplete
    def __init__(self, fid=..., description: str = ..., filename: str = ..., object_data: Incomplete | None = ..., mime_type: Incomplete | None = ...) -> None: ...
    @property
    def description(self): ...
    @description.setter
    def description(self, txt) -> None: ...
    @property
    def mime_type(self): ...
    @mime_type.setter
    def mime_type(self, m) -> None: ...
    @property
    def filename(self): ...
    @filename.setter
    def filename(self, txt) -> None: ...
    encoding: Incomplete
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class PrivateFrame(Frame):
    owner_id: Incomplete
    owner_data: Incomplete
    def __init__(self, id=..., owner_id: bytes = ..., owner_data: bytes = ...) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class MusicCDIdFrame(Frame):
    def __init__(self, id=..., toc: bytes = ...) -> None: ...
    @property
    def toc(self): ...
    data: Incomplete
    @toc.setter
    def toc(self, toc) -> None: ...
    def parse(self, data, frame_header) -> None: ...

class PlayCountFrame(Frame):
    count: Incomplete
    def __init__(self, id=..., count: int = ...) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class PopularityFrame(Frame):
    def __init__(self, id=..., email: bytes = ..., rating: int = ..., count: int = ...) -> None: ...
    @property
    def rating(self): ...
    @rating.setter
    def rating(self, rating) -> None: ...
    @property
    def email(self): ...
    @email.setter
    def email(self, email) -> None: ...
    @property
    def count(self): ...
    @count.setter
    def count(self, count) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class UniqueFileIDFrame(Frame):
    def __init__(self, id=..., owner_id: bytes = ..., uniq_id: bytes = ...) -> None: ...
    @property
    def owner_id(self): ...
    @owner_id.setter
    def owner_id(self, oid) -> None: ...
    @property
    def uniq_id(self): ...
    @uniq_id.setter
    def uniq_id(self, uid) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class LanguageCodeMixin:
    @property
    def lang(self): ...
    @lang.setter
    def lang(self, lang) -> None: ...

class DescriptionLangTextFrame(Frame, LanguageCodeMixin):
    lang: Incomplete
    def __init__(self, id, description, lang, text) -> None: ...
    @property
    def description(self): ...
    @description.setter
    def description(self, description) -> None: ...
    @property
    def text(self): ...
    @text.setter
    def text(self, text) -> None: ...
    encoding: Incomplete
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class CommentFrame(DescriptionLangTextFrame):
    def __init__(self, id=..., description: str = ..., lang=..., text: str = ...) -> None: ...

class LyricsFrame(DescriptionLangTextFrame):
    def __init__(self, id=..., description: str = ..., lang=..., text: str = ...) -> None: ...

class TermsOfUseFrame(Frame, LanguageCodeMixin):
    lang: Incomplete
    def __init__(self, id: bytes = ..., text: str = ..., lang=...) -> None: ...
    @property
    def text(self): ...
    @text.setter
    def text(self, text) -> None: ...
    encoding: Incomplete
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class TocFrame(Frame):
    TOP_LEVEL_FLAG_BIT: int
    ORDERED_FLAG_BIT: int
    element_id: Incomplete
    toplevel: Incomplete
    ordered: Incomplete
    child_ids: Incomplete
    description: Incomplete
    def __init__(self, id=..., element_id: Incomplete | None = ..., toplevel: bool = ..., ordered: bool = ..., child_ids: Incomplete | None = ..., description: Incomplete | None = ...) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...

class RelVolAdjFrameV24(Frame):
    CHANNEL_TYPE_OTHER: int
    CHANNEL_TYPE_MASTER: int
    CHANNEL_TYPE_FRONT_RIGHT: int
    CHANNEL_TYPE_FRONT_LEFT: int
    CHANNEL_TYPE_BACK_RIGHT: int
    CHANNEL_TYPE_BACK_LEFT: int
    CHANNEL_TYPE_FRONT_CENTER: int
    CHANNEL_TYPE_BACK_CENTER: int
    CHANNEL_TYPE_BASS: int
    @property
    def identifier(self): ...
    @identifier.setter
    def identifier(self, ident) -> None: ...
    @property
    def channel_type(self): ...
    @channel_type.setter
    def channel_type(self, t) -> None: ...
    @property
    def adjustment(self): ...
    @adjustment.setter
    def adjustment(self, adj) -> None: ...
    @property
    def peak(self): ...
    @peak.setter
    def peak(self, v) -> None: ...
    def __init__(self, fid: bytes = ..., identifier: Incomplete | None = ..., channel_type: Incomplete | None = ..., adjustment: Incomplete | None = ..., peak: Incomplete | None = ...) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    header: Incomplete
    data: Incomplete
    def render(self): ...

class RelVolAdjFrameV23(Frame):
    FRONT_CHANNEL_RIGHT_BIT: int
    FRONT_CHANNEL_LEFT_BIT: int
    BACK_CHANNEL_RIGHT_BIT: int
    BACK_CHANNEL_LEFT_BIT: int
    FRONT_CENTER_CHANNEL_BIT: int
    BASS_CHANNEL_BIT: int
    CHANNEL_DEFN: Incomplete
    class VolumeAdjustments:
        master: int
        master_peak: int
        front_right: int
        front_left: int
        front_right_peak: int
        front_left_peak: int
        back_right: int
        back_left: int
        back_right_peak: int
        back_left_peak: int
        front_center: int
        front_center_peak: int
        back_center: int
        back_center_peak: int
        bass: int
        bass_peak: int
        other: int
        other_peak: int
        @property
        def has_master_channel(self) -> bool: ...
        @property
        def has_front_channel(self) -> bool: ...
        @property
        def has_back_channel(self) -> bool: ...
        @property
        def has_front_center_channel(self) -> bool: ...
        @property
        def has_back_center_channel(self) -> bool: ...
        @property
        def has_bass_channel(self) -> bool: ...
        @property
        def has_other_channel(self) -> bool: ...
        def boundsCheck(self) -> None: ...
        def setChannelAdj(self, chan_type, value) -> None: ...
        def setChannelPeak(self, chan_type, value) -> None: ...
        def __init__(self, master, master_peak, front_right, front_left, front_right_peak, front_left_peak, back_right, back_left, back_right_peak, back_left_peak, front_center, front_center_peak, back_center, back_center_peak, bass, bass_peak, other, other_peak) -> None: ...
    adjustments: Incomplete
    def __init__(self, fid: bytes = ...) -> None: ...
    def toV24(self) -> list: ...
    def parse(self, data, frame_header) -> None: ...
    header: Incomplete
    data: Incomplete
    def render(self): ...

class StartEndTuple(NamedTuple):
    start: Incomplete
    end: Incomplete

class ChapterFrame(Frame):
    NO_OFFSET: int
    element_id: Incomplete
    times: Incomplete
    offsets: Incomplete
    sub_frames: Incomplete
    def __init__(self, id=..., element_id: Incomplete | None = ..., times: Incomplete | None = ..., offsets: Incomplete | None = ..., sub_frames: Incomplete | None = ...) -> None: ...
    def parse(self, data, frame_header) -> None: ...
    data: Incomplete
    def render(self): ...
    @property
    def title(self): ...
    @title.setter
    def title(self, title) -> None: ...
    @property
    def subtitle(self): ...
    @subtitle.setter
    def subtitle(self, subtitle) -> None: ...
    @property
    def user_url(self): ...
    @user_url.setter
    def user_url(self, url) -> None: ...

class FrameSet(dict):
    def __init__(self) -> None: ...
    def parse(self, f, tag_header, extended_header): ...
    def __getitem__(self, fid): ...
    def __setitem__(self, fid, frame) -> None: ...
    def getAllFrames(self): ...
    def setTextFrame(self, fid, text) -> None: ...
    def __contains__(self, fid): ...

def deunsyncData(data): ...
def createFrame(tag_header, frame_header, data): ...
def decodeUnicode(bites, encoding): ...
def splitUnicode(data, encoding): ...
def id3EncodingToString(encoding): ...
def stringToEncoding(s): ...

ID3_FRAMES: Incomplete

def map2_2FrameId(orig_id): ...

TAGS2_2_TO_TAGS_2_3_AND_4: Incomplete
NONSTANDARD_ID3_FRAMES: Incomplete