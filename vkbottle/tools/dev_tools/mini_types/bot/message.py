from vkbottle_types.objects import MessagesMessage, MessagesClientInfo
from vkbottle_types.events.bot_events import MessageNew
from vkbottle_types import StatePeer
from vkbottle.api import ABCAPI, API
from typing import Optional, Any, List, Union


class MessageMin(MessagesMessage):
    group_id: Optional[int] = None
    client_info: Optional["MessagesClientInfo"] = None
    unprepared_ctx_api: Optional[Any] = None
    state_peer: Optional[StatePeer] = None

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return getattr(self, "unprepared_ctx_api")

    async def answer(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        user_id: Optional[int] = None,
        domain: Optional[str] = None,
        chat_id: Optional[int] = None,
        random_id: Optional[int] = 0,
        user_ids: Optional[List[int]] = None,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        reply_to: Optional[int] = None,
        forward_messages: Optional[List[int]] = None,
        forward: Optional[str] = None,
        sticker_id: Optional[int] = None,
        group_id: Optional[int] = None,
        keyboard: Optional[str] = None,
        payload: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        template: Optional[dict] = None,
        intent: Optional[str] = None,
    ) -> int:
        data = {k: v for k, v in locals().items() if k != "self" and v is not None}
        data["peer_id"] = self.peer_id

        return (await self.ctx_api.request("messages.send", data))["response"]


MessageMin.update_forward_refs()


def message_min(event: dict, ctx_api: "ABCAPI") -> "MessageMin":
    update = MessageNew(**event)
    message = MessageMin(
        **update.object.message.dict(),
        client_info=update.object.client_info.dict(),
        group_id=update.group_id,
    )
    setattr(message, "unprepared_ctx_api", ctx_api)
    return message
