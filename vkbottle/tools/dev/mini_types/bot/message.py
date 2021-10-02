from io import StringIO
from typing import TYPE_CHECKING, Any, List, Optional, Union

from vkbottle_types import StatePeer
from vkbottle_types.events.bot_events import MessageNew
from vkbottle_types.objects import ClientInfoForBots, MessagesForward, MessagesMessage, UsersUser

if TYPE_CHECKING:

    from vkbottle.api import ABCAPI, API


class MessageMin(MessagesMessage):
    group_id: Optional[int] = None
    client_info: Optional["ClientInfoForBots"] = None
    unprepared_ctx_api: Optional[Any] = None
    state_peer: Optional["StatePeer"] = None

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return getattr(self, "unprepared_ctx_api")

    async def get_user(self, raw_mode: bool = False, **kwargs) -> Union["UsersUser", dict]:
        raw_user = (await self.ctx_api.request("users.get", {"user_ids": self.from_id, **kwargs}))[
            "response"
        ][0]
        return raw_user if raw_mode else UsersUser(**raw_user)

    async def answer(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        user_id: Optional[int] = None,
        random_id: Optional[int] = 0,
        peer_id: Optional[int] = None,
        peer_ids: Optional[List[int]] = None,
        domain: Optional[str] = None,
        chat_id: Optional[int] = None,
        user_ids: Optional[List[int]] = None,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        reply_to: Optional[int] = None,
        forward_messages: Optional[List[int]] = None,
        forward: Optional[str] = None,
        sticker_id: Optional[int] = None,
        group_id: Optional[int] = None,
        keyboard: Optional[str] = None,
        template: Optional[str] = None,
        payload: Optional[str] = None,
        content_source: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        intent: Optional[str] = None,
        subscribe_id: Optional[int] = None,
        **kwargs,
    ) -> Optional[int]:
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        required_params = ("peer_id", "user_id", "domain", "chat_id", "user_ids")
        if not any(data.get(param) for param in required_params):
            data["peer_id"] = self.peer_id

        stream = StringIO(message)
        response = None
        while True:
            data["message"] = stream.read(4096)
            if not (data["message"] or data.get("attachment")):
                break
            response = (await self.ctx_api.request("messages.send", data))["response"]
            data.pop("attachment", None)
        return response

    async def reply(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        **kwargs,
    ) -> Optional[int]:
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        data["peer_id"] = self.peer_id
        data["forward"] = MessagesForward(
            conversation_message_ids=[self.conversation_message_id],
            peer_id=self.peer_id,
            is_reply=True,
        ).json()

        return await self.answer(**data)

    async def forward(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        forward_message_ids: Optional[List[int]] = None,
        **kwargs,
    ) -> Optional[int]:
        locals().update(kwargs)

        data = {
            k: v
            for k, v in locals().items()
            if k not in ("self", "kwargs", "forward_message_ids") and v is not None
        }
        if not forward_message_ids:
            forward_message_ids = [self.conversation_message_id]
        data["forward"] = MessagesForward(
            conversation_message_ids=forward_message_ids, peer_id=self.peer_id
        ).json()

        return await self.answer(**data)


MessageMin.update_forward_refs()


def message_min(event: dict, ctx_api: "ABCAPI") -> "MessageMin":
    update = MessageNew(**event)

    if update.object.message is None:
        raise RuntimeError("Please set longpoll to latest version")

    message = MessageMin(
        **update.object.message.dict(),
        client_info=update.object.client_info.dict(),
        group_id=update.group_id,
    )
    setattr(message, "unprepared_ctx_api", ctx_api)
    return message
