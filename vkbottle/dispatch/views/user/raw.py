from typing import TYPE_CHECKING, Dict, List, NamedTuple, Type

from vkbottle_types.events import UserEventType

from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.dispatch.views.abc.raw import ABCRawEventView

if TYPE_CHECKING:
    from vkbottle_types.events import BaseUserEvent

    from vkbottle.dispatch.handlers import ABCHandler


class UserHandlerBasement(NamedTuple):
    dataclass: Type["BaseUserEvent"]
    handler: "ABCHandler"


class RawUserEventView(ABCRawEventView[list]):
    handlers: Dict[UserEventType, List["UserHandlerBasement"]]

    def __init__(self):
        super().__init__()
        self.handlers = {}
        self.handler_return_manager = UserMessageReturnHandler()

    def get_handler_basements(self, event: list) -> List["UserHandlerBasement"]:
        return self.handlers[UserEventType(self.get_event_type(event))]

    def get_event_model(
        self, handler_basement: "UserHandlerBasement", event: list
    ) -> "BaseUserEvent":
        return handler_basement.dataclass(*event)

    @staticmethod
    def get_event_type(event: list) -> int:
        return event[0]

    async def process_event(self, event: list) -> bool:
        try:
            event_type = UserEventType(self.get_event_type(event))
        except ValueError:
            event_type = UserEventType.UNDEFINED_EVENT
        return event_type in self.handlers
