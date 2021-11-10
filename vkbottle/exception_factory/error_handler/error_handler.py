from functools import wraps
from typing import TYPE_CHECKING, Any, Callable, Optional, Type

from .abc import ABCErrorHandler

if TYPE_CHECKING:
    from .abc import AsyncFunc


class ErrorHandler(ABCErrorHandler):
    def __init__(self, redirect_arguments: bool = False):
        self.redirect_arguments = redirect_arguments
        self.error_handlers = {}
        self.undefined_error_handler = None

    def register_error_handler(
        self, *error_types: Type[BaseException]
    ) -> Callable[["AsyncFunc"], "AsyncFunc"]:
        def decorator(handler: "AsyncFunc") -> "AsyncFunc":
            for error_type in error_types:
                self.error_handlers[error_type] = handler
            return handler

        return decorator

    def register_undefined_error_handler(self, handler: "AsyncFunc") -> "AsyncFunc":
        self.undefined_error_handler = handler
        return handler

    def lookup_handler(self, for_type: Type[BaseException]) -> Optional["AsyncFunc"]:
        for error_type in self.error_handlers:
            if issubclass(for_type, error_type):
                return self.error_handlers[error_type]

    async def handle(self, error: BaseException, *args, **kwargs) -> Any:
        handler = self.lookup_handler(type(error)) or self.undefined_error_handler

        if handler is None:
            raise error

        if self.redirect_arguments:
            return await handler(error, *args, **kwargs)
        return await handler(error)

    def catch(self, func: "AsyncFunc") -> "AsyncFunc":
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                await func(*args, **kwargs)
            except BaseException as error:
                return await self.handle(error, *args, **kwargs)

        return wrapper
