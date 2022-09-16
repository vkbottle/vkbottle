from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Coroutine, Dict, Optional, Type, TypeVar

from typing_extensions import ParamSpec

P = ParamSpec("P")

T = TypeVar("T")
T_AsyncFunc = TypeVar("T_AsyncFunc", bound=Callable[..., Awaitable[object]])


class ABCErrorHandler(ABC):
    error_handlers: Dict[Type[Exception], Callable[..., Awaitable[Any]]]
    undefined_error_handler: Optional[Callable[..., Awaitable[Any]]]

    @abstractmethod
    def register_error_handler(
        self, *error_types: Type[Exception]
    ) -> Callable[[T_AsyncFunc], T_AsyncFunc]:
        pass

    @abstractmethod
    def register_undefined_error_handler(self, handler: T_AsyncFunc) -> T_AsyncFunc:
        pass

    @abstractmethod
    async def handle(self, error: Exception) -> Any:
        pass

    @abstractmethod
    def catch(self, func: Callable[P, Awaitable[T]]) -> Callable[P, Coroutine[Any, Any, T]]:
        pass
