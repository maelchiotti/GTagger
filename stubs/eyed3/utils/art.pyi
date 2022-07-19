from ..id3.frames import ImageFrame as ImageFrame
from _typeshed import Incomplete

FRONT_COVER: str
BACK_COVER: str
MISC_COVER: str
LOGO: str
ARTIST: str
LIVE: str
FILENAMES: Incomplete
TO_ID3_ART_TYPES: Incomplete
FROM_ID3_ART_TYPES: Incomplete

def matchArtFile(filename): ...
def getArtFromTag(tag, type_: Incomplete | None = ...): ...
