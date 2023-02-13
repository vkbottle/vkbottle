from abc import ABC, abstractmethod
from typing import Generic, Iterable, Optional, Type, TypeVar, Union

from typing_extensions import Protocol

from vkbottle.tools.dev.utils import call_by_signature

T_contra = TypeVar("T_contra", contravariant=True)


class CleanCheck(Protocol, Generic[T_contra]):
    async def __call__(self, event: T_contra) -> Union[dict, bool, None]:
        ...


class ContextCheck(Protocol, Generic[T_contra]):
    async def __call__(
        self, event: T_contra, context_variables: Optional[dict] = None
    ) -> Union[dict, bool, None]:
        ...


class ABCRule(ABC, Generic[T_contra]):
    config: dict = {}

    @classmethod
    def with_config(cls, config: dict) -> Type["ABCRule"]:
        cls.config = config
        return cls

    @property
    @abstractmethod
    def check(self) -> Union[CleanCheck[T_contra], ContextCheck[T_contra]]:
        ...

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

    async def check(self, event: T_contra, context_variables: Optional[dict] = None):
        inner_context = {}

        for rule in self.rules:
            check_response = await call_by_signature(
                rule.check, event, context_variables=context_variables
            )
            if check_response is False:
                return False
            elif isinstance(check_response, dict):
                inner_context.update(check_response)

        return inner_context

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules


class NotRule(ABCRule[T_contra]):
    def __init__(self, *rules: ABCRule[T_contra]):
        self._rules = rules

    async def check(self, event: T_contra, context_variables: Optional[dict] = None):
        for rule in self.rules:
            check_response = await call_by_signature(
                rule.check, event, context_variables=context_variables
            )
            if check_response is False:
                return True
        return False

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules


class OrRule(ABCRule[T_contra]):
    def __init__(self, *rules: ABCRule[T_contra]):
        self._rules = rules

    async def check(self, event: T_contra, context_variables: Optional[dict] = None):
        for rule in self.rules:
            check_response = await call_by_signature(
                rule.check, event, context_variables=context_variables
            )
            if check_response is not False:
                return check_response
        return False

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules
