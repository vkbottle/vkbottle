from .abc import ABCExceptionFactory
from .code_error import CodeErrorFactory
from .single_error import SingleError
from .error_handler import ABCErrorHandler, ErrorHandler

VKAPIError = CodeErrorFactory("VKAPIError")


class VKBottleError(SingleError):
    pass
