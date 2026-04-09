from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ParamSpec, TypeAlias, TypeVar

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.views.bot import BotHandlerBasement, BotMessageView, RawBotEventView

from .base import BaseLabeler, CustomRuleType

if TYPE_CHECKING:
    from vkbottle_types.events.bot_events import BaseGroupEvent

    from vkbottle.dispatch.views.bot import ABCBotMessageView
    from vkbottle.exception_factory.error_handler import ABCErrorHandler

    EventName: TypeAlias = str | GroupEventType

P = ParamSpec("P")
R = TypeVar("R")


class BotLabeler(BaseLabeler):
    """`BotLabeler` - shortcut manager for router
    Can be loaded to other `BotLabeler`.
    >>> bl = BotLabeler()
    >>> ...
    >>> bl.load(BotLabeler())

    Views are fixed. Custom rules can be set locally (they are
    not inherited to other labelers). Rule config is accessible from
    all custom rules from `ABCRule.config`.
    """

    def __init__(
        self,
        message_view: "ABCBotMessageView[Any] | None" = None,
        raw_event_view: RawBotEventView | None = None,
        custom_rules: CustomRuleType | None = None,
        auto_rules: list["ABCRule[Any]"] | None = None,
        raw_event_auto_rules: list["ABCRule[Any]"] | None = None,
        error_handler: "ABCErrorHandler | None" = None,
    ) -> None:
        message_view = message_view or BotMessageView(error_handler)
        raw_event_view = raw_event_view or RawBotEventView(error_handler)
        super().__init__(
            message_view=message_view,
            raw_event_view=raw_event_view,
            custom_rules=custom_rules,
            auto_rules=auto_rules,
            raw_event_auto_rules=raw_event_auto_rules,
        )

    def message(  # type: ignore
        self,
        *rules: "ABCRule[Any]",
        blocking: bool = True,
        **custom_rules: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        return super().message(*rules, blocking=blocking, **custom_rules)

    def chat_message(  # type: ignore
        self,
        *rules: "ABCRule[Any]",
        blocking: bool = True,
        **custom_rules: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        return super().chat_message(*rules, blocking=blocking, **custom_rules)

    def private_message(  # type: ignore
        self,
        *rules: "ABCRule[Any]",
        blocking: bool = True,
        **custom_rules: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        return super().private_message(*rules, blocking=blocking, **custom_rules)

    def raw_event(  # type: ignore
        self,
        event: "EventName | list[EventName]",
        dataclass: type[dict[str, Any]] | type["BaseGroupEvent"] = dict,
        *rules: "ABCRule[Any]",
        blocking: bool = True,
        **custom_rules: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        if any(not isinstance(rule, ABCRule) for rule in rules):
            msg = (
                "All rules must be subclasses of ABCRule or rule shortcuts "
                "(https://vkbottle.rtfd.io/ru/latest/high-level/handling/rules/)"
            )
            raise ValueError(msg)

        event_types = event if isinstance(event, list) else [event]

        def decorator(func: Any) -> Any:
            for e in event_types:
                if isinstance(e, str):
                    e = GroupEventType(e)

                handler_basement = BotHandlerBasement(
                    dataclass,
                    FromFuncHandler(
                        func,
                        *rules,
                        *self.raw_event_auto_rules,
                        *self.get_custom_rules(custom_rules),
                        blocking=blocking,
                    ),
                )
                event_handlers = self.raw_event_view.handlers.setdefault(e, [])
                event_handlers.append(handler_basement)

            return func

        return decorator  # type: ignore


__all__ = ("BotLabeler",)
