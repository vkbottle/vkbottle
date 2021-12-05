from abc import ABC
from typing import TYPE_CHECKING, Generic, Optional, TypeVar

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.views.abc import ABCMessageView
from vkbottle.tools.dev.mini_types.bot import message_min

if TYPE_CHECKING:
    from vkbottle.tools.dev.mini_types.bot import MessageMin


T_contra = TypeVar("T_contra", contravariant=True)


class ABCBotMessageView(ABCMessageView[dict, T_contra], ABC, Generic[T_contra]):
    def __init__(self):
        super().__init__()
        self.handler_return_manager = BotMessageReturnHandler()

    @staticmethod
    def get_event_type(event: dict) -> str:
        return event["type"]

    @staticmethod
    async def get_message(event, ctx_api) -> "MessageMin":
        return message_min(event, ctx_api)

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(self.get_event_type(event)) == GroupEventType.MESSAGE_NEW


class BotMessageView(ABCBotMessageView["MessageMin"]):
    def get_state_key(self, message: "MessageMin") -> Optional[int]:
        return getattr(message, self.state_source_key, None)
