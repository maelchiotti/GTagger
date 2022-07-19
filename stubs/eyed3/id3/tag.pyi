import string
from . import DEFAULT_LANG as DEFAULT_LANG, Genre as Genre, ID3_ANY_VERSION as ID3_ANY_VERSION, ID3_DEFAULT_VERSION as ID3_DEFAULT_VERSION, ID3_V1 as ID3_V1, ID3_V1_0 as ID3_V1_0, ID3_V1_1 as ID3_V1_1, ID3_V2 as ID3_V2, ID3_V2_2 as ID3_V2_2, ID3_V2_3 as ID3_V2_3, ID3_V2_4 as ID3_V2_4, frames as frames, versionToString as versionToString
from .. import Error as Error, core as core
from ..core import ALBUM_TYPE_IDS as ALBUM_TYPE_IDS, ArtistOrigin as ArtistOrigin, TXXX_ALBUM_TYPE as TXXX_ALBUM_TYPE, TXXX_ARTIST_ORIGIN as TXXX_ARTIST_ORIGIN
from ..utils import b as b, chunkCopy as chunkCopy, datePicker as datePicker, requireUnicode as requireUnicode
from ..utils.log import getLogger as getLogger
from .headers import ExtendedTagHeader as ExtendedTagHeader, TagHeader as TagHeader
from _typeshed import Incomplete
from collections.abc import Generator

log: Incomplete
ID3_V1_COMMENT_DESC: str
ID3_V1_MAX_TEXTLEN: int
ID3_V1_STRIP_CHARS: Incomplete
DEFAULT_PADDING: int

class TagException(Error): ...

class Tag(core.Tag):
    file_info: Incomplete
    header: Incomplete
    extended_header: Incomplete
    frame_set: Incomplete
    def __init__(self, version=..., **kwargs) -> None: ...
    def clear(self, *, version=...) -> None: ...
    def parse(self, fileobj, version=...): ...
    @property
    def version(self): ...
    @version.setter
    def version(self, v) -> None: ...
    def isV1(self): ...
    def isV2(self): ...
    def setTextFrame(self, fid: bytes, txt: str): ...
    def getTextFrame(self, fid: bytes): ...
    @property
    def composer(self): ...
    @composer.setter
    def composer(self, v) -> None: ...
    @property
    def comments(self): ...
    bpm: Incomplete
    @property
    def play_count(self): ...
    @play_count.setter
    def play_count(self, count) -> None: ...
    publisher: Incomplete
    @property
    def cd_id(self): ...
    @cd_id.setter
    def cd_id(self, toc) -> None: ...
    @property
    def images(self): ...
    encoding_date: Incomplete
    @property
    def best_release_date(self): ...
    def getBestDate(self, prefer_recording_date: bool = ...): ...
    release_date: Incomplete
    original_release_date: Incomplete
    recording_date: Incomplete
    tagging_date: Incomplete
    @property
    def lyrics(self): ...
    @property
    def disc_num(self): ...
    @disc_num.setter
    def disc_num(self, val) -> None: ...
    @property
    def objects(self): ...
    @property
    def privates(self): ...
    @property
    def popularities(self): ...
    genre: Incomplete
    non_std_genre: Incomplete
    @property
    def user_text_frames(self): ...
    @property
    def commercial_url(self): ...
    @commercial_url.setter
    def commercial_url(self, url) -> None: ...
    @property
    def copyright_url(self): ...
    @copyright_url.setter
    def copyright_url(self, url) -> None: ...
    @property
    def audio_file_url(self): ...
    @audio_file_url.setter
    def audio_file_url(self, url) -> None: ...
    @property
    def audio_source_url(self): ...
    @audio_source_url.setter
    def audio_source_url(self, url) -> None: ...
    @property
    def artist_url(self): ...
    @artist_url.setter
    def artist_url(self, url) -> None: ...
    @property
    def internet_radio_url(self): ...
    @internet_radio_url.setter
    def internet_radio_url(self, url) -> None: ...
    @property
    def payment_url(self): ...
    @payment_url.setter
    def payment_url(self, url) -> None: ...
    @property
    def publisher_url(self): ...
    @publisher_url.setter
    def publisher_url(self, url) -> None: ...
    @property
    def user_url_frames(self): ...
    @property
    def unique_file_ids(self): ...
    @property
    def terms_of_use(self): ...
    @terms_of_use.setter
    def terms_of_use(self, tos) -> None: ...
    copyright: Incomplete
    encoded_by: Incomplete
    def save(self, filename: Incomplete | None = ..., version: Incomplete | None = ..., encoding: Incomplete | None = ..., backup: bool = ..., preserve_file_time: bool = ..., max_padding: Incomplete | None = ...) -> None: ...
    @staticmethod
    def remove(filename, version=..., preserve_file_time: bool = ...): ...
    @property
    def chapters(self): ...
    @property
    def table_of_contents(self): ...
    @property
    def album_type(self): ...
    @album_type.setter
    def album_type(self, t) -> None: ...
    @property
    def artist_origin(self): ...
    @artist_origin.setter
    def artist_origin(self, origin: ArtistOrigin): ...
    def frameiter(self, fids: Incomplete | None = ...) -> Generator[Incomplete, None, None]: ...
    @property
    def original_artist(self): ...
    @original_artist.setter
    def original_artist(self, name) -> None: ...

class FileInfo:
    name: Incomplete
    tag_size: Incomplete
    tag_padding_size: Incomplete
    def __init__(self, file_name, tagsz: int = ..., tpadd: int = ...) -> None: ...
    def initStatTimes(self) -> None: ...
    def touch(self, times) -> None: ...

class AccessorBase:
    def __init__(self, fid, fs, match_func: Incomplete | None = ...) -> None: ...
    def __iter__(self): ...
    def __len__(self): ...
    def __getitem__(self, i): ...
    def get(self, *args, **kwargs): ...
    def remove(self, *args, **kwargs): ...

class DltAccessor(AccessorBase):
    FrameClass: Incomplete
    def __init__(self, FrameClass, fid, fs): ...
    def set(self, text, description: str = ..., lang=...): ...
    def remove(self, description, lang=...): ...
    def get(self, description, lang=...): ...

class CommentsAccessor(DltAccessor):
    def __init__(self, fs) -> None: ...

class LyricsAccessor(DltAccessor):
    def __init__(self, fs) -> None: ...

class ImagesAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, type_, img_data, mime_type, description: str = ..., img_url: Incomplete | None = ...): ...
    def remove(self, description): ...
    def get(self, description): ...

class ObjectsAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, data, mime_type, description: str = ..., filename: str = ...): ...
    def remove(self, description): ...
    def get(self, description): ...

class PrivatesAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, data, owner_id): ...
    def remove(self, owner_id): ...
    def get(self, owner_id): ...

class UserTextsAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, text, description: str = ...): ...
    def remove(self, description): ...
    def get(self, description): ...
    def __contains__(self, description): ...

class UniqueFileIdAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, data, owner_id): ...
    def remove(self, owner_id): ...
    def get(self, owner_id): ...

class UserUrlsAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, url, description: str = ...): ...
    def remove(self, description): ...
    def get(self, description): ...

class PopularitiesAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, email, rating, play_count): ...
    def remove(self, email): ...
    def get(self, email): ...

class ChaptersAccessor(AccessorBase):
    def __init__(self, fs): ...
    def set(self, element_id, times, offsets=..., sub_frames: Incomplete | None = ...): ...
    def remove(self, element_id): ...
    def get(self, element_id): ...
    def __getitem__(self, elem_id): ...

class TocAccessor(AccessorBase):
    def __init__(self, fs): ...
    def __iter__(self): ...
    def set(self, element_id, toplevel: bool = ..., ordered: bool = ..., child_ids: Incomplete | None = ..., description: str = ...): ...
    def remove(self, element_id): ...
    def get(self, element_id): ...
    def __getitem__(self, elem_id): ...

class TagTemplate(string.Template):
    idpattern: str
    def __init__(self, pattern, path_friendly: str = ..., dotted_dates: bool = ...) -> None: ...
    def substitute(self, tag, zeropad: bool = ...): ...
    safe_substitute: Incomplete
