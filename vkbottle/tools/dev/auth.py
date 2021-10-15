from typing import Optional

from vkbottle.http import SingleAiohttpClient

MOBILE_APP_ID = 2274003
MOBILE_APP_SECRET = "hHbZxrka2uZ6jB1inYsH"


class AuthError(Exception):
    def __init__(self, typ: str, description: str):
        super().__init__(description)
        self.type = typ
        self.description = description


class UserAuth:
    def __init__(self, client_id: Optional[int] = None, client_secret: Optional[str] = None):
        if client_id is not None and client_secret is not None:
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            self.client_id = MOBILE_APP_ID
            self.client_secret = MOBILE_APP_SECRET

    def _build_oauth_url(self, login: str, password: str) -> str:
        return (
            f"https://oauth.vk.com/token?grant_type=password&client_id={self.client_id}"
            f"&client_secret={self.client_secret}&username={login}&password={password}"
        )

    async def get_token(self, login: str, password: str) -> str:
        url = self._build_oauth_url(login, password)

        client = SingleAiohttpClient()
        response = await client.request("get", url)
        json = response.json()

        if "access_token" in json:
            return json["access_token"]

        raise AuthError(json["error"], json["error_description"])
