from typing import TYPE_CHECKING, Generic, Optional, TypeVar, Union

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.return_manager.bot import BotMessageReturnHandler
from vkbottle.dispatch.views.abc import ABCMessageView
from vkbottle.tools.dev.mini_types.bot import message_min

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API
    from vkbottle.tools.dev.mini_types.bot import MessageMin


F_contra = TypeVar("F_contra", contravariant=True)


class ABCBotMessageView(ABCMessageView[dict, F_contra], Generic[F_contra]):
    def __init__(self):
        super().__init__()
        self.handler_return_manager = BotMessageReturnHandler()

    @staticmethod
    def get_event_type(event: dict) -> str:
        return event["type"]

    @staticmethod
    async def get_message(
        event: dict, ctx_api: Union["API", "ABCAPI"], replace_mention: bool
    ) -> "MessageMin":
        return message_min(event, ctx_api, replace_mention)

    async def process_event(self, event: dict) -> bool:
        if not (self.handlers or self.middlewares):
            return False
        typed_event = GroupEventType(self.get_event_type(event))
        return typed_event == GroupEventType.MESSAGE_NEW


class BotMessageView(ABCBotMessageView["MessageMin"]):
    def get_state_key(self, message: "MessageMin") -> Optional[int]:
        return getattr(message, self.state_source_key, None)
