from .artist import Artist as Artist
from .commons import Base as Base
from _typeshed import Incomplete

class Album(Base):
    id: Incomplete
    artist: Incomplete
    cover_art_url: Incomplete
    name: Incomplete
    url: Incomplete
    def __init__(self, genius, data) -> None: ...
