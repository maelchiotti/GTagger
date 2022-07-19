from .api import Sender as Sender
from .errors import InvalidStateError as InvalidStateError
from .utils import parse_redirected_url as parse_redirected_url
from _typeshed import Incomplete

class OAuth2(Sender):
    auth_url: str
    token_url: str
    client_id: Incomplete
    client_secret: Incomplete
    redirect_uri: Incomplete
    scope: Incomplete
    state: Incomplete
    flow: Incomplete
    def __init__(self, client_id, redirect_uri, client_secret: Incomplete | None = ..., scope: Incomplete | None = ..., state: Incomplete | None = ..., client_only_app: bool = ...) -> None: ...
    @property
    def url(self): ...
    def get_user_token(self, code: Incomplete | None = ..., url: Incomplete | None = ..., state: Incomplete | None = ..., **kwargs): ...
    def prompt_user(self): ...
    @classmethod
    def client_only_app(cls, client_id, redirect_uri, scope: Incomplete | None = ..., state: Incomplete | None = ...): ...
    @classmethod
    def full_code_exchange(cls, client_id, redirect_uri, client_secret, scope: Incomplete | None = ..., state: Incomplete | None = ...): ...
