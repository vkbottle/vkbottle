from typing import Dict, NamedTuple, Type

from vkbottle_types.events import BaseUserEvent, UserEventType

from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.dispatch.views.abc import ABCRawEventView

HandlerBasement = NamedTuple(
    "HandlerBasement", [("dataclass", Type[BaseUserEvent]), ("handler", ABCHandler)]
)


class RawEventView(ABCRawEventView):
    def __init__(self):
        super().__init__()
        self.handlers: Dict[UserEventType, HandlerBasement] = {}
        self.handler_return_manager = UserMessageReturnHandler()

    def get_handler_basement(self, event):
        return self.handlers[UserEventType(self.get_event_type(event))]

    def get_event_model(self, handler_basement, event):
        return handler_basement.dataclass(event[1])

    @staticmethod
    def get_event_type(event: list) -> int:
        return event[0]

    async def process_event(self, event: list) -> bool:
        return UserEventType(self.get_event_type(event)) in self.handlers
