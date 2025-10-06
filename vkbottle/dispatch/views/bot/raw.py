import dataclasses
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, Union

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.views.abc.raw import ABCRawEventView, BaseHandlerBasement

if TYPE_CHECKING:
    from vkbottle_types.events.bot_events import BaseGroupEvent

    from vkbottle.dispatch.handlers import ABCHandler
    from vkbottle.exception_factory.error_handler import ABCErrorHandler


@dataclasses.dataclass(frozen=True)
class BotHandlerBasement(BaseHandlerBasement):
    dataclass: Union[Type[dict[str, Any]], Type["BaseGroupEvent"]]
    handler: "ABCHandler"


class RawBotEventView(ABCRawEventView[dict, BotHandlerBasement]):
    handlers: Dict[GroupEventType, List[BotHandlerBasement]]

    def __init__(self, error_handler: Optional["ABCErrorHandler"] = None) -> None:
        super().__init__(error_handler)
        self.handlers = {}
        self.handler_return_manager = BotMessageReturnHandler()

    def get_handler_basements(self, event: dict[str, Any]) -> List[BotHandlerBasement]:
        return self.handlers[GroupEventType(self.get_event_type(event))]

    def get_event_model(
        self,
        handler_basement: BotHandlerBasement,
        event: dict[str, Any],
    ) -> Union[dict[str, Any], "BaseGroupEvent"]:
        return handler_basement.dataclass(**event)

    @staticmethod
    def get_event_type(event: dict[str, Any]) -> str:
        return event["type"]

    async def process_event(self, event: dict[str, Any]) -> bool:
        return GroupEventType(self.get_event_type(event)) in self.handlers


__all__ = ("RawBotEventView",)
