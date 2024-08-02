import dataclasses
from typing import TYPE_CHECKING, Dict, List, Type, Union

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.views.abc.raw import ABCRawEventView, BaseHandlerBasement

if TYPE_CHECKING:
    from vkbottle_types.events.bot_events import BaseGroupEvent

    from vkbottle.dispatch.handlers import ABCHandler


@dataclasses.dataclass(frozen=True)
class BotHandlerBasement(BaseHandlerBasement):
    dataclass: Union[Type[dict], Type["BaseGroupEvent"]]
    handler: "ABCHandler"


class RawBotEventView(ABCRawEventView[dict, BotHandlerBasement]):
    handlers: Dict[GroupEventType, List[BotHandlerBasement]]

    def __init__(self) -> None:
        super().__init__()
        self.handlers = {}
        self.handler_return_manager = BotMessageReturnHandler()

    def get_handler_basements(self, event: dict) -> List[BotHandlerBasement]:
        return self.handlers[GroupEventType(self.get_event_type(event))]

    def get_event_model(
        self,
        handler_basement: BotHandlerBasement,
        event: dict,
    ) -> Union[dict, "BaseGroupEvent"]:
        return handler_basement.dataclass(**event)

    @staticmethod
    def get_event_type(event: dict) -> str:
        return event["type"]

    async def process_event(self, event: dict) -> bool:
        return GroupEventType(self.get_event_type(event)) in self.handlers
