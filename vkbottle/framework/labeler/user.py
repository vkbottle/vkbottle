from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Type, Union

from vkbottle_types.events.enums import UserEventType
from vkbottle_types.events.user_events import RawUserEvent

from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.views.user import RawUserEventView, UserHandlerBasement, UserMessageView

from .base import BaseLabeler

if TYPE_CHECKING:
    from vkbottle_types.events import BaseUserEvent

    from vkbottle.dispatch.rules import ABCRule
    from vkbottle.dispatch.views.user import ABCUserMessageView
    from vkbottle.tools.dev.mini_types.user import MessageMin

    from .abc import LabeledHandler

    LabeledMessageHandler = Callable[..., Callable[["MessageMin"], Any]]
    EventName = Union[UserEventType, str]


class UserLabeler(BaseLabeler):
    """UserLabeler - shortcut manager for router
    Can be loaded to other UserLabeler
    >>> bl = UserLabeler()
    >>> ...
    >>> bl.load(UserLabeler())
    Views are fixed. Custom rules can be set locally (they are
    not inherited to other labelers). Rule config is accessible from
    all custom rules from ABCRule.config
    """

    def __init__(
        self,
        message_view: Optional["ABCUserMessageView"] = None,
        raw_event_view: Optional[RawUserEventView] = None,
        custom_rules: Optional[Dict[str, Type["ABCRule"]]] = None,
        auto_rules: Optional[List["ABCRule"]] = None,
    ):
        message_view = message_view or UserMessageView()
        raw_event_view = raw_event_view or RawUserEventView()
        super().__init__(
            message_view=message_view,
            raw_event_view=raw_event_view,
            custom_rules=custom_rules,
            auto_rules=auto_rules,
        )

    def message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        return super().message(*rules, blocking=blocking, **custom_rules)

    def chat_message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        return super().chat_message(*rules, blocking=blocking, **custom_rules)

    def private_message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> "LabeledMessageHandler":
        return super().private_message(*rules, blocking=blocking, **custom_rules)

    def raw_event(
        self,
        event: Union[int, List[int], UserEventType, List[UserEventType]],
        dataclass: Type["BaseUserEvent"] = RawUserEvent,
        *rules: "ABCRule",
        blocking: bool = True,
        **custom_rules,
    ) -> "LabeledHandler":

        if not isinstance(event, list):
            event = [event]

        def decorator(func):
            for e in event:
                if isinstance(e, int):
                    e = UserEventType(e)
                handler_basement = UserHandlerBasement(
                    dataclass,
                    FromFuncHandler(
                        func,
                        *rules,
                        *self.auto_rules,
                        *self.get_custom_rules(custom_rules),
                        blocking=blocking,
                    ),
                )
                event_handlers = self.raw_event_view.handlers.setdefault(e, [])
                event_handlers.append(handler_basement)
            return func

        return decorator
