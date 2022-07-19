from .__about__ import __version__ as version
from .core import load as load
from .utils.log import log as log
from _typeshed import Incomplete

LOCAL_ENCODING: Incomplete
LOCAL_FS_ENCODING: Incomplete

class Error(Exception):
    message: Incomplete
    def __init__(self, *args) -> None: ...
