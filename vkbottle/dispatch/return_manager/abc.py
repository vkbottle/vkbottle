from abc import ABC
from typing import Dict, Callable, Coroutine, Any, Union, Tuple, Optional, NamedTuple


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
        handlers = {}
        for k, v in vars(self.__class__).items():
            if not isinstance(v, HandlerProperty):
                continue
            handlers[v.types] = v.handler
        return handlers

    @classmethod
    def instance_of(
        cls, types: Union[type, Tuple[type, ...]]
    ) -> Callable[[Callable], HandlerProperty]:
        def decorator(func: Callable):
            return HandlerProperty(types, func)

        return decorator

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"
