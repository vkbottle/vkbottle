from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Awaitable, Callable, Dict, NamedTuple, Optional, Tuple, Union

HANDLER_PROPERTY_TYPES = Union[type, Tuple[type, ...]]


class HandlerProperty(NamedTuple):
    types: HANDLER_PROPERTY_TYPES
    handler: Callable


# TODO: fix types here
class ABCRetunManager(ABC):
    @abstractmethod
    def get_handler(self, value: Any) -> Any:
        ...

    @abstractproperty
    def handlers(self) -> Any:
        ...

    @classmethod
    @abstractmethod
    def instance_of(cls, types: Any) -> Any:
        ...

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class BaseReturnManager(ABCRetunManager):
    def get_handler(self, value: Any) -> Optional[Callable]:
        for types, handler in self.handlers.items():
            if isinstance(value, types):
                return handler

    @property
    def handlers(self) -> Dict[HANDLER_PROPERTY_TYPES, Callable[[Any], Awaitable]]:
        return {
            v.types: v.handler
            for k, v in vars(self.__class__).items()
            if isinstance(v, HandlerProperty)
        }

    @classmethod
    def instance_of(
        cls, types: Union[type, Tuple[type, ...]]
    ) -> Callable[[Callable], HandlerProperty]:
        def decorator(func: Callable):
            return HandlerProperty(types, func)

        return decorator
