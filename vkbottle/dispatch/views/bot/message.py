from abc import ABC
from typing import Optional

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.views.abc import ABCMessageView
from vkbottle.tools.dev.mini_types.bot import MessageMin, message_min


class ABCBotMessageView(ABCMessageView, ABC):
    def __init__(self):
        super().__init__()
        self.handler_return_manager = BotMessageReturnHandler()

    @staticmethod
    def get_event_type(event):
        return event.get("event_id")

    @staticmethod
    async def get_message(event, ctx_api):
        return message_min(event, ctx_api)

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(event["type"]) == GroupEventType.MESSAGE_NEW


class BotMessageView(ABCBotMessageView):
    def get_state_key(self, message: MessageMin) -> Optional[int]:
        return getattr(message, self.state_source_key, None)
