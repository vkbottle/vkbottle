from typing import TYPE_CHECKING, Any, Generic, Optional, TypeVar, Union

from vkbottle_types.events import UserEventType

from vkbottle.dispatch.return_manager.user import UserMessageReturnHandler
from vkbottle.dispatch.views.abc.message import ABCMessageView
from vkbottle.tools.mini_types.user import message_min

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API
    from vkbottle.exception_factory.error_handler import ABCErrorHandler
    from vkbottle.tools.mini_types.user import MessageMin

F_contra = TypeVar("F_contra", contravariant=True)


class ABCUserMessageView(ABCMessageView[list[Any], F_contra], Generic[F_contra]):
    def __init__(self, error_handler: Optional["ABCErrorHandler"] = None) -> None:
        super().__init__(error_handler)
        self.handler_return_manager = UserMessageReturnHandler()

    @staticmethod
    def get_event_type(event: list[Any]) -> int:
        return event[0]

    @staticmethod
    async def get_message(
        event: list[Any],
        ctx_api: Union["API", "ABCAPI"],
        replace_mention: bool,
    ) -> "MessageMin":
        return await message_min(event[1], ctx_api, replace_mention)

    async def process_event(self, event: list[Any]) -> bool:
        if not (self.handlers or self.middlewares):
            return False
        try:
            event_type = UserEventType(self.get_event_type(event))
        except ValueError:
            return False
        return event_type == UserEventType.MESSAGE_NEW


class UserMessageView(ABCUserMessageView["MessageMin"]):
    def get_state_key(self, message: "MessageMin") -> Optional[int]:
        return getattr(message, self.state_source_key, None)


__all__ = ("ABCUserMessageView", "UserMessageView")
