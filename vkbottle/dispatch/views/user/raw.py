import dataclasses
from typing import TYPE_CHECKING, Any, Dict, List, Type

from vkbottle_types.events import UserEventType

from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.dispatch.views.abc.raw import ABCRawEventView, BaseHandlerBasement

if TYPE_CHECKING:
    from vkbottle_types.events.user_events import BaseUserEvent

    from vkbottle.dispatch.handlers import ABCHandler


@dataclasses.dataclass(frozen=True)
class UserHandlerBasement(BaseHandlerBasement):
    dataclass: Type["BaseUserEvent"]
    handler: "ABCHandler"


class RawUserEventView(ABCRawEventView[List[Any], UserHandlerBasement]):
    handlers: Dict[UserEventType, List[UserHandlerBasement]]

    def __init__(self) -> None:
        super().__init__()
        self.handlers = {}
        self.handler_return_manager = UserMessageReturnHandler()

    def get_handler_basements(self, event: List[Any]) -> List[UserHandlerBasement]:
        return self.handlers[UserEventType(self.get_event_type(event))]

    def get_event_model(
        self,
        handler_basement: UserHandlerBasement,
        event: List[Any],
    ) -> "BaseUserEvent":
        return handler_basement.dataclass.parse(event[1:])

    @staticmethod
    def get_event_type(event: List[Any]) -> int:
        return event[0]

    async def process_event(self, event: List[Any]) -> bool:
        try:
            event_type = UserEventType(self.get_event_type(event))
        except ValueError:
            event_type = UserEventType.UNDEFINED_EVENT

        return event_type in self.handlers
