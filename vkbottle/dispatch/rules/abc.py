from abc import ABC, abstractmethod
from typing import Generic, Iterable, Type, TypeVar

T_contra = TypeVar("T_contra", contravariant=True)


class ABCRule(ABC, Generic[T_contra]):
    config: dict = {}

    @classmethod
    def with_config(cls, config: dict) -> Type["ABCRule"]:
        cls.config = config
        return cls

    @abstractmethod
    async def check(self, event: T_contra):
        pass

    def __and__(self, other: "ABCRule[T_contra]") -> "AndRule[T_contra]":
        return AndRule(self, other)

    def __or__(self, other: "ABCRule[T_contra]") -> "OrRule[T_contra]":
        return OrRule(self, other)

    def __invert__(self) -> "NotRule[T_contra]":
        return NotRule(self)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}>"


class AndRule(ABCRule[T_contra], Generic[T_contra]):
    def __init__(self, *rules: ABCRule[T_contra]):
        self._rules = rules

    async def check(self, event: T_contra):
        context = {}

        for rule in self.rules:
            check_response = await rule.check(event)
            if check_response is False:
                return False
            elif isinstance(check_response, dict):
                context.update(check_response)

        return context

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules


class NotRule(ABCRule[T_contra]):
    def __init__(self, *rules: ABCRule[T_contra]):
        self._rules = rules

    async def check(self, event: T_contra):
        for rule in self.rules:
            check_response = await rule.check(event)
            if check_response is False:
                return True
        return False

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules


class OrRule(ABCRule[T_contra]):
    def __init__(self, *rules: ABCRule[T_contra]):
        self._rules = rules

    async def check(self, event: T_contra):
        for rule in self.rules:
            check_response = await rule.check(event)
            if check_response is not False:
                return check_response
        return False

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules
