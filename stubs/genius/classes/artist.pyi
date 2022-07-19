from .commons import Base as Base
from .social_media import SocialMedia as SocialMedia
from _typeshed import Incomplete
from typing import Dict, Iterator, List

def lazy_property(prop): ...

class Artist(Base):
    id: Incomplete
    header_image_url: Incomplete
    image_url: Incomplete
    is_verified: Incomplete
    name: Incomplete
    url: Incomplete
    def __init__(self, genius, data) -> None: ...
    def __init_extra_data__(self, data) -> None: ...
    def alternate_names(self) -> List[str]: ...
    def description(self) -> str: ...
    def followers_count(self) -> int: ...
    def social_media(self) -> Dict[str, SocialMedia]: ...
    @property
    def songs(self) -> Iterator['Song']: ...
    @property
    def songs_by_popularity(self) -> Iterator['Song']: ...
