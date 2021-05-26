import typing
from abc import ABC, abstractmethod

ExceptionHandler = typing.Callable[[BaseException], typing.Awaitable[typing.Any]]


class ABCErrorHandler(ABC):
    error_handlers: typing.Any

    @abstractmethod
    def register_error_handler(
        self,
        exception_type: typing.Type[BaseException],
        exception_handler: ExceptionHandler = None,
    ) -> typing.Optional[typing.Callable[[ExceptionHandler], typing.Any]]:
        pass

    @abstractmethod
    def register_undefined_error_handler(
        self, exception_handler: typing.Optional[ExceptionHandler] = None,
    ) -> typing.Optional[typing.Callable[[ExceptionHandler], typing.Any]]:
        pass

    @abstractmethod
    async def handle(self, e: BaseException) -> typing.Any:
        pass

    @abstractmethod
    def wraps_error_handler(
        self,
    ) -> typing.Callable[
        [typing.Any], typing.Callable[[typing.Any, typing.Any], typing.Awaitable[typing.Any]]
    ]:
        pass

    @property
    @abstractmethod
    def handling_exceptions(self,) -> typing.Union[str, typing.Tuple[str, ...]]:
        pass
