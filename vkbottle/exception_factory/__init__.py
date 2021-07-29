from typing import Dict, Any

from .code_exception import CodeException
from .error_handler import ABCErrorHandler, ErrorHandler
from .swear_handler import swear


class VKAPIError(CodeException):
    def __init__(self, description: str):
        self.description = description
