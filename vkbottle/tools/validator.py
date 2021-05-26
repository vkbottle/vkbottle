from abc import ABC, abstractmethod
from typing import Any, Callable, Tuple, Union


class ABCValidator(ABC):
    @abstractmethod
    async def check(self, value: Any) -> bool:
        pass


class IsInstanceValidator(ABCValidator):
    def __init__(self, t: Union[type, Tuple[type, ...]]):
        self.t = t

    async def check(self, value: Any) -> bool:
        return isinstance(value, self.t)


class EqualsValidator(ABCValidator):
    def __init__(self, primary_value: Any):
        self.primary_value = primary_value

    async def check(self, value: Any) -> bool:
        return value == self.primary_value


class CallableValidator(ABCValidator):
    def __init__(self, call: Callable[[Any], bool]):
        self.call = call

    async def check(self, value: Any) -> bool:
        return self.call(value)
