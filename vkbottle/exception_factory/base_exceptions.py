from typing import List, Optional

from vkbottle.modules import logger

from .code_exception import CodeException
from .reducible_kwargs_exception import ReducibleKwargsException


class VKAPIError(CodeException, ReducibleKwargsException):
    def __init__(self, *, error_msg: str, request_params: Optional[List[dict]] = None, **kwargs):
        self.error_msg = error_msg
        # server maybe return error code without request_params key
        if request_params:
            self.request_params = {item["key"]: item["value"] for item in request_params}
        else:
            self.request_params = {}
        if kwargs:
            logger.warning("VK API Error {} has extra kwargs: {}", self.code, kwargs)
        self.kwargs = kwargs

    def __str__(self) -> str:
        return self.error_msg


class CaptchaError(VKAPIError, code=14):
    def __init__(
        self,
        *,
        captcha_sid: str,
        captcha_img: str,
        captcha_ts: Optional[str] = None,
        captcha_attempt: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.captcha_sid = int(captcha_sid)
        self.captcha_img = captcha_img
        self.captcha_ts = captcha_ts
        self.captcha_attempt = captcha_attempt


class APIAuthError(VKAPIError, code=5):
    def __init__(self, *, ban_info: Optional[dict] = None, **kwargs):
        super().__init__(**kwargs)
        self.ban_info = ban_info
