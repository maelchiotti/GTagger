from .artist import Artist as Artist
from .base import BaseEntity as BaseEntity, Stats as Stats
from _typeshed import Incomplete

class Song(BaseEntity):
    artist: Incomplete
    lyrics: Incomplete
    primary_artist: Incomplete
    stats: Incomplete
    annotation_count: Incomplete
    api_path: Incomplete
    full_title: Incomplete
    header_image_thumbnail_url: Incomplete
    header_image_url: Incomplete
    lyrics_owner_id: Incomplete
    lyrics_state: Incomplete
    path: Incomplete
    pyongs_count: Incomplete
    song_art_image_thumbnail_url: Incomplete
    song_art_image_url: Incomplete
    title: Incomplete
    title_with_featured: Incomplete
    url: Incomplete
    def __init__(self, client, json_dict, lyrics: str = ...) -> None: ...
    def to_dict(self): ...
    def to_json(self, filename: Incomplete | None = ..., sanitize: bool = ..., ensure_ascii: bool = ...): ...
    def to_text(self, filename: Incomplete | None = ..., sanitize: bool = ...): ...
    def save_lyrics(self, filename: Incomplete | None = ..., extension: str = ..., overwrite: bool = ..., ensure_ascii: bool = ..., sanitize: bool = ..., verbose: bool = ...): ...
    def __cmp__(self, other): ...
