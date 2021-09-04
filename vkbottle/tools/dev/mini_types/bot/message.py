from typing import Any, List, Optional, Union

from vkbottle_types import StatePeer
from vkbottle_types.events.bot_events import MessageNew
from vkbottle_types.objects import ClientInfoForBots, MessagesForward, MessagesMessage, UsersUser

from vkbottle.api import ABCAPI, API


class MessageMin(MessagesMessage):
    group_id: Optional[int] = None
    client_info: Optional["MessagesClientInfo"] = None
    unprepared_ctx_api: Optional[Any] = None
    state_peer: Optional[StatePeer] = None

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
        template: Optional[str] = None,
        intent: Optional[str] = None,
        **kwargs,
    ) -> int:
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        data["peer_id"] = self.peer_id

        return (await self.ctx_api.request("messages.send", data))["response"]

    async def reply(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        user_id: Optional[int] = None,
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
        payload: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        **kwargs,
    ) -> int:
        locals().update(kwargs)
        locals().pop("kwargs")
        data = {k: v for k, v in locals().items() if k != "self" and v is not None}
        data["peer_id"] = self.peer_id
        data["forward"] = MessagesForward(
            conversation_message_ids=[self.conversation_message_id],
            peer_id=self.peer_id,
            is_reply=True
        ).json()

        return (await self.ctx_api.request("messages.send", data))["response"]

    async def forward(
        self,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        peer_id: Optional[int] = None,
        user_id: Optional[int] = None,
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
        payload: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        **kwargs,
    ) -> int:
        locals().update(kwargs)
        locals().pop("kwargs")
        data = {k: v for k, v in locals().items() if k != "self" and v is not None}
        required_params = ("peer_id", "user_id", "domain", "chat_id", "user_ids")
        if not any(data.get(param) for param in required_params):
            data["peer_id"] = self.peer_id
        data["forward"] = MessagesForward(
            conversation_message_ids=[self.conversation_message_id],
            peer_id=self.peer_id
        ).json()

        return (await self.ctx_api.request("messages.send", data))["response"]

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
