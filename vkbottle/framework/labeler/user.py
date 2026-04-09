from collections.abc import Callable
from typing import TYPE_CHECKING, Any, ParamSpec, TypeVar

from vkbottle_types.events.enums import UserEventType
from vkbottle_types.events.user_events import RawUserEvent

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.views.user import RawUserEventView, UserHandlerBasement, UserMessageView

from .base import BaseLabeler, CustomRuleType

if TYPE_CHECKING:
    from typing_extensions import TypeAlias
    from vkbottle_types.events.user_events import BaseUserEvent

    from vkbottle.dispatch.views.user import ABCUserMessageView
    from vkbottle.exception_factory.error_handler import ABCErrorHandler

    EventName: TypeAlias = UserEventType | str

P = ParamSpec("P")
R = TypeVar("R")


class UserLabeler(BaseLabeler):
    """`UserLabeler` - shortcut manager for router
    Can be loaded to other `UserLabeler`.
    >>> bl = UserLabeler()
    >>> ...
    >>> bl.load(UserLabeler())

    Views are fixed. Custom rules can be set locally (they are
    not inherited to other labelers). Rule config is accessible from
    all custom rules from `ABCRule.config`.
    """

    def __init__(
        self,
        message_view: "ABCUserMessageView[Any] | None" = None,
        raw_event_view: RawUserEventView | None = None,
        custom_rules: CustomRuleType | None = None,
        auto_rules: list["ABCRule[Any]"] | None = None,
        raw_event_auto_rules: list["ABCRule[Any]"] | None = None,
        error_handler: "ABCErrorHandler | None" = None,
    ) -> None:
        message_view = message_view or UserMessageView(error_handler)
        raw_event_view = raw_event_view or RawUserEventView(error_handler)
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
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules: Any,
    ) -> Callable[[Callable[P, R]], Callable[P, R]]:
        return super().private_message(*rules, blocking=blocking, **custom_rules)

    def raw_event(  # type: ignore
        self,
        event: int | list[int] | UserEventType | list[UserEventType],
        dataclass: type["BaseUserEvent"] = RawUserEvent,
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

        event_types = [event] if isinstance(event, (int, UserEventType)) else event

        def decorator(func: Any) -> Any:
            for e in event_types:
                if isinstance(e, int):
                    e = UserEventType(e)

                handler_basement = UserHandlerBasement(
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


__all__ = ("UserLabeler",)
