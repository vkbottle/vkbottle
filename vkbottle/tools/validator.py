from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any


class ABCValidator(ABC):
    @abstractmethod
    async def check(self, value: Any) -> bool:
        pass


class IsInstanceValidator(ABCValidator):
    def __init__(self, t: type[Any] | tuple[type[Any], ...]):
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


__all__ = ("ABCValidator", "CallableValidator", "EqualsValidator", "IsInstanceValidator")
