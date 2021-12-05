from io import StringIO
from typing import TYPE_CHECKING, Any, List, Optional, Union

from vkbottle_types import StatePeer
from vkbottle_types.objects import MessagesMessage, UsersUser

if TYPE_CHECKING:

    from vkbottle.api import ABCAPI, API


class BaseMessageMin(MessagesMessage):
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
    ) -> int:
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        required_params = ("peer_id", "user_id", "domain", "chat_id", "user_ids")
        if not any(data.get(param) for param in required_params):
            data["peer_id"] = self.peer_id

        stream = StringIO(message)
        while True:
            msg = stream.read(4096)
            if msg:
                data["message"] = msg
            response = (await self.ctx_api.request("messages.send", data))["response"]
            if stream.tell() == len(message or ""):
                break
        return response


BaseMessageMin.update_forward_refs()
