from .base import Sender as Sender
from .public_methods import AlbumMethods as AlbumMethods, AnnotationMethods as AnnotationMethods, ArticleMethods as ArticleMethods, ArtistMethods as ArtistMethods, CoverArtMethods as CoverArtMethods, DiscussionMethods as DiscussionMethods, LeaderboardMethods as LeaderboardMethods, MiscMethods as MiscMethods, QuestionMethods as QuestionMethods, ReferentMethods as ReferentMethods, SearchMethods as SearchMethods, SongMethods as SongMethods, UserMethods as UserMethods, VideoMethods as VideoMethods
from _typeshed import Incomplete

class API(Sender):
    def __init__(self, access_token, response_format: str = ..., timeout: int = ..., sleep_time: float = ..., retries: int = ...) -> None: ...
    def account(self, text_format: Incomplete | None = ...): ...
    def annotation(self, annotation_id, text_format: Incomplete | None = ...): ...
    def create_annotation(self, text, raw_annotatable_url, fragment, before_html: Incomplete | None = ..., after_html: Incomplete | None = ..., canonical_url: Incomplete | None = ..., og_url: Incomplete | None = ..., title: Incomplete | None = ..., text_format: Incomplete | None = ...): ...
    def delete_annotation(self, annotation_id): ...
    def downvote_annotation(self, annotation_id, text_format: Incomplete | None = ...): ...
    def unvote_annotation(self, annotation_id, text_format: Incomplete | None = ...): ...
    def update_annotation(self, annotation_id, text, raw_annotatable_url, fragment, before_html: Incomplete | None = ..., after_html: Incomplete | None = ..., canonical_url: Incomplete | None = ..., og_url: Incomplete | None = ..., title: Incomplete | None = ..., text_format: Incomplete | None = ...): ...
    def upvote_annotation(self, annotation_id, text_format: Incomplete | None = ...): ...
    def artist(self, artist_id, text_format: Incomplete | None = ...): ...
    def artist_songs(self, artist_id, per_page: Incomplete | None = ..., page: Incomplete | None = ..., sort: str = ...): ...
    def referents(self, song_id: Incomplete | None = ..., web_page_id: Incomplete | None = ..., created_by_id: Incomplete | None = ..., per_page: Incomplete | None = ..., page: Incomplete | None = ..., text_format: Incomplete | None = ...): ...
    def search_songs(self, search_term, per_page: Incomplete | None = ..., page: Incomplete | None = ...): ...
    def song(self, song_id, text_format: Incomplete | None = ...): ...
    def web_page(self, raw_annotatable_url: Incomplete | None = ..., canonical_url: Incomplete | None = ..., og_url: Incomplete | None = ...): ...

class PublicAPI(Sender, AlbumMethods, AnnotationMethods, ArticleMethods, ArtistMethods, CoverArtMethods, DiscussionMethods, LeaderboardMethods, QuestionMethods, ReferentMethods, SearchMethods, SongMethods, UserMethods, VideoMethods, MiscMethods):
    def __init__(self, response_format: str = ..., timeout: int = ..., sleep_time: float = ..., retries: int = ..., **kwargs) -> None: ...
