from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any, ClassVar, Generic, Type, TypeVar

from vkbottle.tools.magic import magic_bundle

T_contra = TypeVar("T_contra", contravariant=True)


class ABCRule(ABC, Generic[T_contra]):
    config: ClassVar[dict] = {}

    @classmethod
    def with_config(cls, config: dict) -> Type[ABCRule]:
        cls.config = config
        return cls

    @abstractmethod
    async def check(
        self, event: T_contra, /, *args: Any, **kwargs: Any
    ) -> bool | dict[str, Any] | None: ...

    def __and__(self, other: ABCRule[T_contra]) -> AndRule[T_contra]:
        return AndRule(self, other)

    def __or__(self, other: ABCRule[T_contra]) -> OrRule[T_contra]:
        return OrRule(self, other)

    def __invert__(self) -> NotRule[T_contra]:
        return NotRule(self)

    def __repr__(self) -> str:
        return "<{}>".format(f"{self.__class__.__module__}.{self.__class__.__name__}")


class AndRule(ABCRule[T_contra], Generic[T_contra]):
    def __init__(self, *rules: ABCRule[T_contra]):
        self._rules = rules

    async def check(self, event: T_contra, context: dict[str, Any]):
        rule_ctx = dict[str, Any]()

        for rule in self.rules:
            check_response = await rule.check(
                event,
                **magic_bundle(rule.check, rule_ctx | context),
            )
            if check_response is False:
                return False
            elif isinstance(check_response, dict):
                rule_ctx.update(check_response)

        return rule_ctx

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules


class NotRule(ABCRule[T_contra]):
    def __init__(self, *rules: ABCRule[T_contra]):
        self._rules = rules

    async def check(self, event: T_contra, context: dict[str, Any]):
        for rule in self.rules:
            check_response = await rule.check(
                event,
                **magic_bundle(rule.check, context),
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

    async def check(self, event: T_contra, context: dict[str, Any]):
        for rule in self.rules:
            check_response = await rule.check(
                event,
                **magic_bundle(rule.check, context),
            )
            if check_response is not False:
                return check_response
        return False

    @property
    def rules(self) -> Iterable[ABCRule[T_contra]]:
        return self._rules


__all__ = ("ABCRule", "AndRule", "NotRule", "OrRule")
