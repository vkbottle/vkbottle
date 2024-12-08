from typing import Any, List, Optional

from vkbottle.modules import logger

from .code_exception import CodeException
from .reducible_kwargs_exception import ReducibleKwargsException


class VKAPIError(CodeException, ReducibleKwargsException):
    def __init__(
        self, *, error_msg: str, request_params: Optional[List[dict]] = None, **kwargs: Any
    ):
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
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.captcha_sid = captcha_sid
        self.captcha_img = captcha_img
        self.captcha_ts = captcha_ts
        self.captcha_attempt = captcha_attempt


class APIAuthError(VKAPIError, code=5):
    def __init__(
        self,
        *,
        validation_type: Optional[str] = None,
        validation_sid: Optional[str] = None,
        phone_mask: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        ban_info: Optional[dict] = None,
        error_description: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.validation_type = validation_type
        self.validation_sid = validation_sid
        self.phone_mask = phone_mask
        self.redirect_uri = redirect_uri
        self.ban_info = ban_info
        self.error_description = error_description
