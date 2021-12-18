from io import StringIO
from typing import TYPE_CHECKING, Any, List, Optional, Union

from vkbottle_types.events.objects.group_event_objects import MessageEventObject

from vkbottle.dispatch.dispenser.base import StatePeer
from vkbottle.tools.dev.event_data import OpenAppEvent, OpenLinkEvent, ShowSnackbarEvent

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

    EventDataType = Union[ShowSnackbarEvent, OpenAppEvent, OpenLinkEvent]


class MessageEventMin(MessageEventObject):
    unprepared_ctx_api: Optional[Any] = None
    state_peer: Optional["StatePeer"] = None
    group_id: Optional[int] = None

    def __init__(self, **event):
        data = event["object"]
        data["group_id"] = event["group_id"]

        super().__init__(**data)

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return getattr(self, "unprepared_ctx_api")

    async def send_message_event_answer(self, event_data: "EventDataType", **kwargs) -> int:
        data = dict(
            event_id=self.event_id,
            user_id=self.user_id,
            peer_id=self.peer_id,
            event_data=event_data.json(),
        )
        data.update(kwargs)
        return (await self.ctx_api.request("messages.sendMessageEventAnswer", data))["response"]

    async def show_snackbar(self, text: str) -> int:
        return await self.send_message_event_answer(ShowSnackbarEvent(text=text))

    async def open_link(self, link: str) -> int:
        return await self.send_message_event_answer(OpenLinkEvent(link=link))

    async def open_app(self, app_id: int, app_hash: str, owner_id: Optional[int] = None) -> int:
        return await self.send_message_event_answer(
            OpenAppEvent(app_id=app_id, hash=app_hash, owner_id=owner_id)
        )

    async def edit_message(
        self,
        message: Optional[str] = None,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        attachment: Optional[str] = None,
        keep_forward_messages: Optional[bool] = None,
        keep_snippets: Optional[bool] = None,
        dont_parse_links: Optional[bool] = None,
        template: Optional[str] = None,
        keyboard: Optional[str] = None,
        **kwargs,
    ) -> int:
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        data["peer_id"] = self.peer_id
        data["conversation_message_id"] = self.conversation_message_id
        return (await self.ctx_api.request("messages.edit", data))["response"]

    async def send_message(
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


MessageEventMin.update_forward_refs()
