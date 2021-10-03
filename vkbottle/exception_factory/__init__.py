from typing import Any

from pydantic.validators import int_validator, str_validator

from .code_exception import CodeException
from .error_handler import ABCErrorHandler, ErrorHandler
from .swear_handler import swear


class VKAPIError(CodeException):
    def __init__(self, *, error_msg: Any):
        super().__init__(error_msg)
        self.description = str_validator(error_msg)


class CaptchaError(VKAPIError[14]):  # type: ignore
    def __init__(self, *, captcha_sid: Any, captcha_img: Any, **kwargs):
        super().__init__(**kwargs)
        self.sid = int_validator(captcha_sid)
        self.img = str_validator(captcha_img)
