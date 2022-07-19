from .commons import Base as Base
from _typeshed import Incomplete

class Media(Base):
    provider: Incomplete
    type: Incomplete
    url: Incomplete
    def __init__(self, genius, data) -> None: ...
