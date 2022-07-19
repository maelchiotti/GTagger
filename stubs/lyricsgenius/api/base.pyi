from _typeshed import Incomplete

class Sender:
    API_ROOT: str
    PUBLIC_API_ROOT: str
    WEB_ROOT: str
    authorization_header: Incomplete
    access_token: Incomplete
    response_format: Incomplete
    timeout: Incomplete
    sleep_time: Incomplete
    retries: Incomplete
    def __init__(self, access_token: Incomplete | None = ..., response_format: str = ..., timeout: int = ..., sleep_time: float = ..., retries: int = ..., public_api_constructor: bool = ...) -> None: ...

def get_description(e): ...
