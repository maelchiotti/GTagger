from _typeshed import Incomplete

class APIException(Exception):
    status: Incomplete
    message: Incomplete
    url: Incomplete
    def __init__(self, status, message, url) -> None: ...
