from typing import List

from .code_exception import CodeException


class VKAPIError(CodeException):
    def __init__(self, *, error_msg: str, request_params: List[dict]):
        self.description = error_msg
        self.params = {item["key"]: item["value"] for item in request_params}

    def __str__(self) -> str:
        return self.description


class CaptchaError(VKAPIError, code=14):
    def __init__(self, *, captcha_sid: str, captcha_img: str, **kwargs):
        super().__init__(**kwargs)
        self.sid = int(captcha_sid)
        self.img = captcha_img
