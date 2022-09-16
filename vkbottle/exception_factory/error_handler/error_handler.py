from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, Optional, Type, TypeVar

from typing_extensions import ParamSpec

from vkbottle.modules import logger

from .abc import ABCErrorHandler

P = ParamSpec("P")

T = TypeVar("T")
T_AsyncFunc = TypeVar("T_AsyncFunc", bound=Callable[..., Awaitable[object]])


class ErrorHandler(ABCErrorHandler):
    def __init__(self, redirect_arguments: bool = False, raise_exceptions: bool = False):
        self.redirect_arguments = redirect_arguments
        self.raise_exceptions = raise_exceptions
        self.error_handlers = {}
        self.undefined_error_handler = None

    def register_error_handler(
        self, *error_types: Type[Exception]
    ) -> Callable[[T_AsyncFunc], T_AsyncFunc]:
        def decorator(handler: T_AsyncFunc) -> T_AsyncFunc:
            for error_type in error_types:
                self.error_handlers[error_type] = handler
            return handler

        return decorator

    def register_undefined_error_handler(self, handler: T_AsyncFunc) -> T_AsyncFunc:
        self.undefined_error_handler = handler
        return handler

    def lookup_handler(self, for_type: Type[Exception]) -> Optional[Callable[..., Awaitable[Any]]]:
        for error_type in self.error_handlers:
            if issubclass(for_type, error_type):
                return self.error_handlers[error_type]

    async def handle(self, error: Exception, *args, **kwargs) -> Any:
        handler = self.lookup_handler(type(error)) or self.undefined_error_handler

        if not handler:
            if self.raise_exceptions:
                raise error
            logger.exception(error)
            return

        if self.redirect_arguments:
            return await handler(error, *args, **kwargs)
        return await handler(error)

    def catch(self, func: Callable[P, Awaitable[T]]) -> Callable[P, Coroutine[Any, Any, T]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as error:
                return await self.handle(error, *args, **kwargs)

        return wrapper
