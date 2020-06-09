import types
import typing

from vkbottle.types import BaseModel
from vkbottle.utils import logger, names
from .middleware import Middleware, MiddlewareFlags


class MiddlewareExecutor:
    def __init__(self):
        self.middleware: typing.List[typing.Union[Middleware, typing.Callable]] = []

    def add_middleware(self, middleware: typing.Union[Middleware, typing.Callable]):
        if middleware is None:
            return
        self.middleware.append(middleware)

    def middleware_handler(self, *context):
        def wrapper(cls):
            if not isinstance(cls, types.FunctionType):
                self.middleware.append(cls(*context))
            else:
                self.middleware.append(cls)
            return cls

        return wrapper

    def export_middleware(self, middleware_list: typing.List[Middleware]):
        self.middleware.extend(middleware_list)

    async def run_middleware(
        self, event: BaseModel, flag: MiddlewareFlags, *middleware_args
    ):
        for middleware in self.middleware:
            logger.debug(
                f"Executing middleware {middleware.__class__.__name__} ({str(flag)})"
            )
            yield await middleware.emulate_middleware(event, flag, *middleware_args)

    def __repr__(self):
        return f"<MiddlewareExecutor middleware={', '.join(names(self.middleware))}>"
