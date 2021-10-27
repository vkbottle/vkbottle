from abc import ABC
from typing import TYPE_CHECKING, Optional

from vkbottle_types.events import UserEventType

from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.dispatch.views.abc.message import ABCMessageView
from vkbottle.tools.dev.mini_types.user import message_min

if TYPE_CHECKING:
    from vkbottle.tools.dev.mini_types.user import MessageMin


class ABCUserMessageView(ABCMessageView, ABC):
    def __init__(self):
        super().__init__()
        self.handler_return_manager = UserMessageReturnHandler()

    @staticmethod
    def get_event_type(event: list) -> int:
        return event[0]

    @staticmethod
    async def get_message(event, ctx_api) -> "MessageMin":
        return await message_min(event[1], ctx_api)

    async def process_event(self, event: list) -> bool:
        if not (self.handlers or self.middlewares):
            return False
        try:
            event_type = UserEventType(self.get_event_type(event))
        except ValueError:
            event_type = UserEventType.UNDEFINED_EVENT
        return event_type == UserEventType.MESSAGE_NEW


class UserMessageView(ABCUserMessageView):
    def get_state_key(self, message: "MessageMin") -> Optional[int]:
        return getattr(message, self.state_source_key, None)
