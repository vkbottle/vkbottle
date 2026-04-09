from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Generic, ParamSpec, TypeVar

if TYPE_CHECKING:
    from vkbottle.dispatch.rules import ABCRule
    from vkbottle.dispatch.views import ABCView
    from vkbottle.dispatch.views.abc import ABCMessageView, ABCRawEventView
    from vkbottle.tools.mini_types.base import BaseMessageMin

E = TypeVar("E", bound="BaseMessageMin")
P = ParamSpec("P")
R = TypeVar("R")


class ABCLabeler(ABC, Generic[E]):
    message_view: "ABCMessageView[Any, Any]"
    raw_event_view: "ABCRawEventView[Any, Any]"
    custom_rules: dict[str, type["ABCRule[Any]"]]
    auto_rules: list["ABCRule[Any]"]
    raw_event_auto_rules: list["ABCRule[Any]"]
    rule_config: dict[str, Any]

    @abstractmethod
    def message(
        self, *rules: "ABCRule[Any]", **custom_rules: Any
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        pass

    @abstractmethod
    def chat_message(
        self, *rules: "ABCRule[Any]", **custom_rules: Any
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        pass

    @abstractmethod
    def private_message(
        self,
        *rules: "ABCRule[Any]",
        **custom_rules: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        pass

    @abstractmethod
    def raw_event(
        self,
        event: str | list[str],
        dataclass: Any,
        *rules: "ABCRule[Any]",
        **custom_rules: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        pass

    @abstractmethod
    def views(self) -> dict[str, "ABCView[Any]"]:
        pass

    @abstractmethod
    def load(self, labeler: Any) -> None:
        pass


__all__ = ("ABCLabeler",)
