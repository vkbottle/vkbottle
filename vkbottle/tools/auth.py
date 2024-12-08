from __future__ import annotations

from enum import IntEnum
from functools import reduce
from typing import TYPE_CHECKING

from vkbottle_types import API_URL, API_VERSION

from vkbottle.exception_factory import APIAuthError, CaptchaError, VKAPIError

if TYPE_CHECKING:
    from typing import Any, List, Optional, Union

    from vkbottle.http import ABCHTTPClient

MOBILE_APP_ID = 2274003
MOBILE_APP_SECRET = "hHbZxrka2uZ6jB1inYsH"  # noqa: S105


class AuthError(VKAPIError[0]):  # type: ignore
    def __init__(
        self,
        *,
        error_msg: str,
        error_description: str,
        error_type: Optional[str] = None,
        view: Optional[str] = None,
        request_params: Optional[List[dict]] = None,
        **kwargs: Any,
    ) -> None:
        request_params = request_params or []
        super().__init__(error_msg=error_msg, request_params=request_params, **kwargs)
        self.error_msg = error_msg
        self.error_description = error_description
        self.error_type = error_type
        self.view = view


class UserPermission(IntEnum):
    notify = 0
    friends = 1
    photos = 2
    audio = 3
    video = 4
    stories = 6
    pages = 7
    menu = 8
    wallmenu = 9
    status = 10
    notes = 11
    messages = 12
    wall = 13
    ads = 15
    offline = 16
    docs = 17
    groups = 18
    notifications = 19
    stats = 20
    email = 22
    adsweb = 23
    leads = 24
    exchange = 26
    market = 27
    phone_number = 28


DEFAULT_USER_PERMISSIONS = [
    UserPermission.friends,
    UserPermission.photos,
    UserPermission.video,
    UserPermission.stories,
    UserPermission.pages,
    UserPermission.status,
    UserPermission.notes,
    UserPermission.wall,
    UserPermission.ads,
    UserPermission.offline,
    UserPermission.docs,
    UserPermission.groups,
    UserPermission.notifications,
    UserPermission.stats,
    UserPermission.email,
    UserPermission.adsweb,
    UserPermission.exchange,
    UserPermission.market,
]


def get_scope(permissions: Union[int, List[UserPermission]]) -> int:
    if isinstance(permissions, int):
        return permissions

    return reduce(lambda x, y: x + 2**y, permissions, 0)


class UserAuth:
    AUTH_URL = "https://oauth.vk.com/token"

    def __init__(
        self,
        client_id: Optional[int] = None,
        client_secret: Optional[str] = None,
        language: str = "en",
        http_client: Optional["ABCHTTPClient"] = None,
    ) -> None:
        from vkbottle.http import SingleAiohttpClient

        if client_id is not None and client_secret is not None:
            self.client_id = client_id
            self.client_secret = client_secret
        else:
            self.client_id = MOBILE_APP_ID
            self.client_secret = MOBILE_APP_SECRET

        self.language = language

        self.http_client = http_client or SingleAiohttpClient()

    def _get_params(
        self,
        login: str,
        password: str,
        scope: Optional[Union[int, List[UserPermission]]] = None,
        auth_code: Union[bool, str] = False,
        captcha_sid: Optional[str] = None,
        captcha_key: Optional[str] = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        params = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": login,
            "password": password,
            "scope": get_scope(scope or DEFAULT_USER_PERMISSIONS),
            "lang": self.language,
        }

        if auth_code:
            params.update(
                {
                    "2fa_supported": 1,
                    "force_sms": 1,
                }
            )
            if isinstance(auth_code, str):
                params["code"] = auth_code

        if captcha_sid and captcha_key:
            params.update(
                {
                    "captcha_sid": captcha_sid,
                    "captcha_key": captcha_key,
                }
            )

        params.update(kwargs)

        return params

    async def get_token(
        self,
        login: str,
        password: str,
        scope: Optional[Union[int, List[UserPermission]]] = None,
        auth_code: Union[bool, str] = False,
        captcha_sid: Optional[str] = None,
        captcha_key: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        params = self._get_params(
            login=login,
            password=password,
            scope=scope,
            auth_code=auth_code,
            captcha_sid=captcha_sid,
            captcha_key=captcha_key,
            kwargs=kwargs,
        )

        response = await self.http_client.request_json(
            url=self.AUTH_URL,
            method="POST",
            data=params,
        )

        if "access_token" in response:
            return response["access_token"]

        response["error_msg"] = response.pop("error")
        error_msg = response["error_msg"]
        if error_msg == "need_captcha":
            raise CaptchaError(**response, request_params=[])
        if error_msg == "need_validation":
            raise APIAuthError(**response, request_params=[])
        raise AuthError(**response, request_params=[])

    async def validate_phone(
        self,
        validation_sid: str,
        api_version: str = API_VERSION,
    ) -> dict[str, Any]:
        response = await self.http_client.request_json(
            url=API_URL + "auth.validatePhone",
            params={
                "sid": validation_sid,
                "lang": self.language,
                "v": api_version,
            },
        )

        error: str | dict[str, Any] | None = response.pop("error", None)
        if not error:
            return response

        if isinstance(error, dict) and "error_code" in error:
            raise VKAPIError[error.pop("error_code")](**error)

        response["error_msg"] = error
        raise AuthError(**response, request_params=[])


__all__ = ("AuthError", "UserAuth", "UserPermission")
