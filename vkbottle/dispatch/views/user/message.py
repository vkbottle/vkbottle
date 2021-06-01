from typing import Optional

from vkbottle_types.events import UserEventType

from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.dispatch.views.abc.message import ABCMessageView
from vkbottle.tools.dev_tools.mini_types.user import MessageMin, message_min


class ABCUserMessageView(ABCMessageView):
    def __init__(self):
        super().__init__()
        self.handler_return_manager = UserMessageReturnHandler()

    @staticmethod
    def get_logger_event_value(event):
        return event[0]

    @staticmethod
    async def get_message(event, ctx_api):
        return await message_min(event[1], ctx_api)

    async def process_event(self, event: int) -> bool:
        return UserEventType(event) == UserEventType.NEW_MESSAGE


class MessageView(ABCUserMessageView):
    def get_state_key(self, message: MessageMin) -> Optional[int]:
        return getattr(message, self.state_source_key, None)
