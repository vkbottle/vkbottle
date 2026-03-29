from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any, NamedTuple

HANDLER_PROPERTY_TYPES = type | tuple[type, ...]


class HandlerProperty(NamedTuple):
    types: HANDLER_PROPERTY_TYPES
    handler: Callable


class ABCReturnManager(ABC):
    @abstractmethod
    def get_handler(self, value: Any) -> Any: ...

    @property
    @abstractmethod
    def handlers(self) -> Any: ...

    @classmethod
    @abstractmethod
    def instance_of(cls, types: Any) -> Any: ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class BaseReturnManager(ABCReturnManager):
    def get_handler(self, value: Any) -> Callable | None:
        for types, handler in self.handlers.items():
            if isinstance(value, types):
                return handler

    @property
    def handlers(self) -> dict[HANDLER_PROPERTY_TYPES, Callable[[Any], Awaitable]]:
        return {
            v.types: v.handler
            for k, v in vars(self.__class__).items()
            if isinstance(v, HandlerProperty)
        }

    @classmethod
    def instance_of(
        cls,
        types: type | tuple[type, ...],
    ) -> Callable[[Callable], HandlerProperty]:
        def decorator(func: Callable):
            return HandlerProperty(types, func)

        return decorator


__all__ = ("ABCReturnManager", "BaseReturnManager")
