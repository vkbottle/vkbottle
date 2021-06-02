from random import randint
from typing import Any, List, Optional, Union

from vkbottle_types import StatePeer
from vkbottle_types.objects import MessagesMessage, UsersUser

from vkbottle.api import ABCAPI, API


class MessageMin(MessagesMessage):
    user_id: Optional[int] = None
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
        data["random_id"] = randint(-2000000000, 2000000000)
        data["peer_id"] = self.peer_id

        return (await self.ctx_api.request("messages.send", data))["response"]


MessageMin.update_forward_refs()


async def message_min(message_id: int, ctx_api: "ABCAPI") -> "MessageMin":
    message_object = (await ctx_api.request("messages.getById", {"message_ids": message_id}))[
        "response"
    ]["items"][0]
    message = MessageMin(**message_object)
    setattr(message, "unprepared_ctx_api", ctx_api)
    return message
