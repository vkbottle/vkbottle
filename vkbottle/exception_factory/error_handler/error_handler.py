import traceback
import typing

from vkbottle.modules import logger

from .abc import ABCErrorHandler, ExceptionHandler


class ErrorHandler(ABCErrorHandler):
    def __init__(self, redirect_arguments: bool = False):
        self.error_handlers: typing.Dict[str, ExceptionHandler] = {}
        self.undefined_error_handler: typing.Optional[ExceptionHandler] = None
        self.redirect_arguments = redirect_arguments

    def register_error_handler(
        self,
        exception_type: typing.Type[BaseException],
        exception_handler: typing.Optional[ExceptionHandler] = None,
    ) -> typing.Optional[typing.Callable[[ExceptionHandler], typing.Any]]:

        if exception_handler:
            self.error_handlers[exception_type.__name__] = exception_handler
            return None

        def decorator(func: ExceptionHandler):
            self.error_handlers[exception_type.__name__] = func
            return func

        return decorator

    def register_undefined_error_handler(
        self, undefined_error_handler: typing.Optional[ExceptionHandler] = None,
    ) -> typing.Optional[typing.Callable[[ExceptionHandler], typing.Any]]:

        if undefined_error_handler:
            self.undefined_error_handler = undefined_error_handler
            return None

        def decorator(func: ExceptionHandler):
            self.undefined_error_handler = func
            return func

        return decorator

    async def call_handler(
        self, handler: ExceptionHandler, e: BaseException, *args, **kwargs
    ) -> typing.Awaitable[typing.Any]:
        if self.redirect_arguments:
            return await handler(e, *args, **kwargs)  # type: ignore
        return await handler(e)  # type: ignore

    def wraps_error_handler(
        self,
    ) -> typing.Callable[
        [typing.Any], typing.Callable[[typing.Any, typing.Any], typing.Awaitable[typing.Any]]
    ]:
        def decorator(func: typing.Union[typing.NoReturn, typing.Any]):
            async def wrapper(*args, **kwargs):
                try:
                    return await func(*args, **kwargs)
                except BaseException as e:
                    return await self.handle(e, *args, **kwargs)

            return wrapper

        return decorator

    async def handle(self, e: BaseException, *args, **kwargs) -> typing.Any:
        if e.__class__.__name__ in self.error_handlers:
            return await self.call_handler(
                self.error_handlers[e.__class__.__name__], e, *args, **kwargs
            )
        elif self.undefined_error_handler:
            return await self.call_handler(self.undefined_error_handler, e, *args, **kwargs)
        logger.error("\n" + traceback.format_exc())

    @property
    def handling_exceptions(self,) -> typing.Union[str, typing.Tuple[str, ...]]:
        return tuple(k for k in self.error_handlers.keys())
