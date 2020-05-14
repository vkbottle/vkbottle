import typing
from abc import ABC, abstractmethod

from vkbottle.utils import ContextInstanceMixin
from vkbottle.utils.exceptions import VKError

CAPTCHA_ERROR_CODE = 14
ErrorHandler = typing.Callable[[VKError], typing.Awaitable]


class VKErrorHandler(ABC, ContextInstanceMixin):
    def __init__(self):
        self.handled_errors: typing.Dict[int, ErrorHandler] = {}
        self.handled_captcha: typing.Optional[ErrorHandler] = None
        self._captcha_delayed: bool = False

    def captcha_handler(self, func: typing.Callable[[VKError], typing.Awaitable[str]]):
        self.handled_captcha = func
        return func

    async def handle_error(self, e: VKError):
        """ Handle errors with added error handlers / undefined error handler """
        if e.error_code == CAPTCHA_ERROR_CODE and self.handled_captcha is not None:
            key = await self.handled_captcha(e)
            response = await self.call_method_with_captcha(e, key)
            return {"response": response}
        elif e.error_code not in self.handled_errors:
            return await self.unhandled_error(e)
        return {"response": await self.handled_errors[e.error_code](e)}

    def error_handler(self, error_code: int):
        def decorator(func):
            self.handled_errors[error_code] = func
            return func

        return decorator

    def add_error_handler(self, error_code: int, handler: typing.Callable):
        """ Add handler for error with specified error_code """
        self.handled_errors[error_code] = handler

    @abstractmethod
    async def unhandled_error(self, e: VKError):
        pass

    @staticmethod
    async def call_method_with_captcha(e: VKError, key: str):
        method = e.method_requested
        method.kwargs = {"captcha_sid": e.raw_error["captcha_sid"], "captcha_key": key}
        return await method(**e.params_requested)

    def __repr__(self):
        return f"<VKErrorHandler handled_errors={tuple(self.handled_errors.keys())} captcha_handler={self.handled_captcha}>"


class DefaultErrorHandler(VKErrorHandler):
    async def unhandled_error(self, e: VKError):
        raise e
