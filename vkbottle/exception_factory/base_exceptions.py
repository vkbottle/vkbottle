from typing import List, Optional

from .code_exception import CodeException


class VKAPIError(CodeException):
    def __init__(self, *, error_msg: str, request_params: Optional[List[dict]] = None):
        self.description = error_msg
        # server maybe return error code without request_params key
        if request_params:
            self.params = {item["key"]: item["value"] for item in request_params}
        else:
            self.params = {}

    def __str__(self) -> str:
        return self.description


class CaptchaError(VKAPIError, code=14):
    def __init__(self, *, captcha_sid: str, captcha_img: str, **kwargs):
        super().__init__(**kwargs)
        self.sid = int(captcha_sid)
        self.img = captcha_img
