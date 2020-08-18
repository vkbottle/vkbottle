from typing import Optional
from aiohttp import BasicAuth
from vkbottle.utils import ContextInstanceMixin


class Proxy(ContextInstanceMixin):
    def __init__(
        self, address: str, login: Optional[str] = None, password: Optional[str] = None
    ):
        self.address = address
        self.login = login
        self.password = password

        self.set_current(self)

    def get_auth(self, encoding: str = "latin1") -> Optional[BasicAuth]:
        if self.login and self.password:
            return BasicAuth(
                login=self.login, password=self.password, encoding=encoding
            )

    def get_proxy(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f"<Proxy {self.address}>"
