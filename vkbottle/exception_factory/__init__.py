from .abc import ABCExceptionFactory
from .code_error import CodeErrorFactory
from .error_handler import ABCErrorHandler, ErrorHandler

VKAPIError = CodeErrorFactory()
