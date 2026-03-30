from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable, Coroutine
from typing import Any, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")
T = TypeVar("T")
T_AsyncFunc = TypeVar("T_AsyncFunc", bound=Callable[..., Awaitable[object]])


class ABCErrorHandler(ABC):
    error_handlers: dict[type[Exception], Callable[..., Awaitable[Any]]]
    undefined_error_handler: Callable[..., Awaitable[Any]] | None

    @abstractmethod
    def register_error_handler(
        self, *error_types: type[Exception]
    ) -> Callable[[T_AsyncFunc], T_AsyncFunc]:
        pass

    @abstractmethod
    def register_undefined_error_handler(self, handler: T_AsyncFunc) -> T_AsyncFunc:
        pass

    @abstractmethod
    async def handle(self, error: Exception, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def catch(self, func: Callable[P, Awaitable[T]]) -> Callable[P, Coroutine[Any, Any, T]]:
        pass


__all__ = ("ABCErrorHandler",)
