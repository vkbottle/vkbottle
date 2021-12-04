from typing import TYPE_CHECKING, Dict, List, NamedTuple, Type, Union

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.views.abc.raw import ABCRawEventView

if TYPE_CHECKING:
    from vkbottle_types.events import BaseGroupEvent

    from vkbottle.dispatch.handlers import ABCHandler


class BotHandlerBasement(NamedTuple):
    dataclass: Union[Type[dict], Type["BaseGroupEvent"]]
    handler: "ABCHandler"


class RawBotEventView(ABCRawEventView[dict]):
    handlers: Dict[GroupEventType, List["BotHandlerBasement"]]

    def __init__(self):
        super().__init__()
        self.handlers = {}
        self.handler_return_manager = BotMessageReturnHandler()

    def get_handler_basements(self, event: dict) -> List["BotHandlerBasement"]:
        return self.handlers[GroupEventType(self.get_event_type(event))]

    def get_event_model(
        self, handler_basement: "BotHandlerBasement", event: dict
    ) -> Union[dict, "BaseGroupEvent"]:
        return handler_basement.dataclass(**event)

    @staticmethod
    def get_event_type(event: dict) -> str:
        return event["type"]

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(self.get_event_type(event)) in self.handlers
