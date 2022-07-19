import logging
from _typeshed import Incomplete

DEFAULT_FORMAT: str
MAIN_LOGGER: str

class Logger(logging.Logger):
    propagate: bool
    def __init__(self, name) -> None: ...
    def verbose(self, msg, *args, **kwargs) -> None: ...

def getLogger(name): ...

log: Incomplete

def initLogging(): ...

LEVELS: Incomplete
