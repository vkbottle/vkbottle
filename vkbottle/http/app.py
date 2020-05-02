from vkbottle.api.exceptions import VKError
from .request import HTTP
import typing

APPS = {
    "android": {"client_id": 2274003, "client_secret": "hHbZxrka2uZ6jB1inYsH"},
    "iphone": {"client_id": 3140623, "client_secret": "VeWdmVclDCtn6ihuP1nt"},
    "desktop": {"client_id": 3697615, "client_secret": "AlVXZFMUqyrnABp8ncuU"},
}


class App(HTTP):
    def __init__(self, login: str, password: str):
        self._login = login
        self._password = password
        self._tokens: typing.List[str] = []

    async def __call__(self, limit: int = 3) -> list:
        for k, v in APPS.items():
            response = await self.request.get(
                "https://oauth.vk.com/token"
                "?grant_type=password"
                f"&client_id={v['client_id']}"
                f"&client_secret={v['client_secret']}"
                f"&username={self._login}"
                f"&password={self._password}"
            )
            if "error" in response:
                raise VKError(response["error_description"])
            if len(self._tokens) < limit:
                self._tokens.append(response["access_token"])
        return self._tokens
