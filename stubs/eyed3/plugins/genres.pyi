from _typeshed import Incomplete
from eyed3 import id3 as id3
from eyed3.plugins import Plugin as Plugin

class GenreListPlugin(Plugin):
    SUMMARY: str
    DESCRIPTION: str
    NAMES: Incomplete
    def __init__(self, arg_parser) -> None: ...
    def start(self, args, config) -> None: ...
