from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Iterable, Type

if TYPE_CHECKING:
    from vkbottle_types.events import Event


class ABCRule(ABC):
    config: dict = {}

    @classmethod
    def with_config(cls, config: dict) -> Type["ABCRule"]:
        cls.config = config
        return cls

    @abstractmethod
    async def check(self, event: "Event"):
        pass

    def __and__(self, other: "ABCRule") -> "ABCFilter":
        return AndFilter(self, other)

    def __or__(self, other: "ABCRule") -> "ABCFilter":
        return OrFilter(self, other)

    def __repr__(self):
        return f"<{self.__class__.__qualname__}>"


class ABCFilter(ABCRule):
    @property
    @abstractmethod
    def rules(self) -> Iterable[ABCRule]:
        pass


class AndFilter(ABCFilter):
    def __init__(self, *rules: ABCRule):
        self._rules = rules

    async def check(self, event: Any):
        context = {}

        for rule in self.rules:
            check_response = await rule.check(event)
            if check_response is False:
                return False
            elif isinstance(check_response, dict):
                context.update(check_response)

        return context

    @property
    def rules(self) -> Iterable[ABCRule]:
        return self._rules


class OrFilter(ABCFilter):
    def __init__(self, *rules: ABCRule):
        self._rules = rules

    async def check(self, event: Any):
        for rule in self.rules:
            check_response = await rule.check(event)
            if check_response is not False:
                return check_response
        return False

    @property
    def rules(self) -> Iterable[ABCRule]:
        return self._rules
