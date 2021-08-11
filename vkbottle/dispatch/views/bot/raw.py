from typing import Dict, List, NamedTuple, Type, Union

from vkbottle_types.events import BaseGroupEvent, GroupEventType

from vkbottle.dispatch.handlers import ABCHandler
from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.views.abc import ABCRawEventView


class HandlerBasement(NamedTuple):
    dataclass: Union[dict, Type[BaseGroupEvent]]
    handler: ABCHandler


class RawBotEventView(ABCRawEventView):
    def __init__(self):
        super().__init__()
        self.handlers: Dict[GroupEventType, List[HandlerBasement]] = {}
        self.handler_return_manager = BotMessageReturnHandler()

    def get_handler_basements(self, event):
        return self.handlers[GroupEventType(self.get_event_type(event))]

    def get_event_model(self, handler_basement, event):
        return handler_basement.dataclass(**event)

    @staticmethod
    def get_event_type(event: dict) -> str:
        return event["type"]

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(self.get_event_type(event)) in self.handlers
