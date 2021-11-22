from typing import Any, List

from pydantic.validators import int_validator, str_validator

from .code_exception import CodeException


class VKAPIError(CodeException):
    def __init__(self, *, error_msg: Any, request_params: List[dict]):
        super().__init__(error_msg)
        self.description = str_validator(error_msg)
        self.params = {item["key"]: item["value"] for item in request_params}


class CaptchaError(VKAPIError[14]):  # type: ignore
    def __init__(self, *, captcha_sid: Any, captcha_img: Any, **kwargs):
        super().__init__(**kwargs)
        self.sid = int_validator(captcha_sid)
        self.img = str_validator(captcha_img)
