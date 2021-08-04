from .code_exception import CodeException
from .error_handler import ABCErrorHandler, ErrorHandler
from .swear_handler import swear


class VKAPIError(CodeException):
    def __init__(self, description: str, raw_error: dict):
        super().__init__(description)
        self.description = description
        self.raw_error = raw_error
