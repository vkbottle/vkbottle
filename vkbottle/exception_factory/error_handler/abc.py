from abc import ABC, abstractmethod
import typing


ExceptionHandler = typing.Optional[typing.Callable[[BaseException], typing.Awaitable[typing.Any]]]


class ABCErrorHandler(ABC):
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
    def wraps_error_handler(
        self,
    ) -> typing.Callable[
        [typing.Any], typing.Callable[[typing.Any, typing.Any], typing.Awaitable[typing.Any]]
    ]:
        pass
