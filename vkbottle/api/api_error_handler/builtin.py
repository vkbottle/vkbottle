from .abc import ABCAPIErrorHandler
from vkbottle.exception_factory import VKAPIError
import typing


class BuiltinAPIErrorHandler(ABCAPIErrorHandler):
    def __init__(self):
        self.error_handlers: typing.Dict[int, "ABCAPIErrorHandler.ErrorHandler"] = {}
        self.undefined_error_handler: "ABCAPIErrorHandler.ErrorHandler" = self.default_undefined_error_handler

    @staticmethod
    async def default_undefined_error_handler(e: VKAPIError, _: dict):  # type: ignore
        raise e

    async def handle_error(self, code: int, description: str, data: dict):
        error = VKAPIError(code, description)

        if code not in self.error_handlers:
            return await self.undefined_error_handler(error, data)
        return await self.error_handlers[code](error, data)

    def register_api_error_handler(
        self, code: int, error_handler: "ABCAPIErrorHandler.ErrorHandler"
    ) -> typing.NoReturn:
        self.error_handlers[code] = error_handler
