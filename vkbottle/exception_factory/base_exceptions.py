from typing import List, Optional

from .code_exception import CodeException
from .reducible_kwargs_exception import ReducibleKwargsException


class VKAPIError(CodeException, ReducibleKwargsException):
    def __init__(self, *, error_msg: str, request_params: Optional[List[dict]] = None):
        self.error_msg = error_msg
        # server maybe return error code without request_params key
        if request_params:
            self.request_params = {item["key"]: item["value"] for item in request_params}
        else:
            self.request_params = {}

    def __str__(self) -> str:
        return self.error_msg


class CaptchaError(VKAPIError, code=14):
    def __init__(self, *, captcha_sid: str, captcha_img: str, **kwargs):
        super().__init__(**kwargs)
        self.captcha_sid = int(captcha_sid)
        self.captcha_img = captcha_img


class APIAuthError(VKAPIError, code=5):
    def __init__(self, *, ban_info: Optional[dict] = None, **kwargs):
        super().__init__(**kwargs)
        self.ban_info = ban_info
