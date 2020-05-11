from abc import ABC, abstractmethod
from vkbottle.utils.exceptions import VKError
import typing
import traceback
from vkbottle.utils import logger


class VKErrorHandler(ABC):
    def __init__(self):
        self.handled_errors: typing.Dict[int, typing.Callable] = {}

    async def handle_error(self, e: VKError):
        if e.error_code not in self.handled_errors:
            return await self.unhandled_error(e)
        return await self.handled_errors[e.error_code](e)

    def add_error_handler(self, error_code: int, handler: typing.Callable):
        self.handled_errors[error_code] = handler

    @abstractmethod
    async def unhandled_error(self, e: VKError):
        pass

    def __repr__(self):
        return f"<VKErrorHandler handled_errors={tuple(self.handled_errors.keys())}>"


class DefaultErrorHandler(VKErrorHandler):
    async def unhandled_error(self, e: VKError):
        logger.error(traceback.format_exc(2))
