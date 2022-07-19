from .frames import Frame as Frame, TextFrame as TextFrame
from _typeshed import Incomplete

PCST_FID: bytes
WFED_FID: bytes
TKWD_FID: bytes
TDES_FID: bytes
TGID_FID: bytes
GRP1_FID: bytes

class PCST(Frame):
    def __init__(self, _: Incomplete | None = ...) -> None: ...
    data: Incomplete
    def render(self): ...

class TKWD(TextFrame):
    def __init__(self, _: Incomplete | None = ..., **kwargs) -> None: ...

class TDES(TextFrame):
    def __init__(self, _: Incomplete | None = ..., **kwargs) -> None: ...

class TGID(TextFrame):
    def __init__(self, _: Incomplete | None = ..., **kwargs) -> None: ...

class WFED(TextFrame):
    def __init__(self, _: Incomplete | None = ..., url: str = ...) -> None: ...

class GRP1(TextFrame):
    def __init__(self, _: Incomplete | None = ..., **kwargs) -> None: ...
