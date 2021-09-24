from typing import TYPE_CHECKING, Dict, List, NamedTuple, Type, Union

from vkbottle_types.events import UserEventType

from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.dispatch.views.abc import ABCRawEventView

if TYPE_CHECKING:
    from vkbottle_types.events import BaseUserEvent

    from vkbottle.dispatch.handlers import ABCHandler


class HandlerBasement(NamedTuple):
    dataclass: Union[dict, Type["BaseUserEvent"]]
    handler: "ABCHandler"


class RawUserEventView(ABCRawEventView):
    def __init__(self):
        super().__init__()
        self.handlers: Dict[UserEventType, List[HandlerBasement]] = {}
        self.handler_return_manager = UserMessageReturnHandler()

    def get_handler_basements(self, event) -> List[HandlerBasement]:
        return self.handlers[UserEventType(self.get_event_type(event))]

    def get_event_model(self, handler_basement, event) -> Union[dict, Type["BaseUserEvent"]]:
        return handler_basement.dataclass(event[1])

    @staticmethod
    def get_event_type(event: list) -> int:
        return event[0]

    async def process_event(self, event: list) -> bool:
        return UserEventType(self.get_event_type(event)) in self.handlers
