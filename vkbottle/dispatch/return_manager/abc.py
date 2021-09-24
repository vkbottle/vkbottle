from abc import ABC
from typing import Any, Callable, Coroutine, Dict, NamedTuple, Optional, Tuple, Union

HandlerProperty = NamedTuple(
    "HandlerProperty", (("types", Union[type, Tuple[type, ...]]), ("handler", Callable))
)


class BaseReturnManager(ABC):
    def get_handler(self, value: Any) -> Optional[Callable]:
        for types, handler in self.handlers.items():
            if isinstance(value, types):
                return handler

    @property
    def handlers(self) -> Dict[Union[type, Tuple[type, ...]], Callable[[Any], Coroutine]]:
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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
