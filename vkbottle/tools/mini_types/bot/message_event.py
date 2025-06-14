from io import StringIO
from typing import TYPE_CHECKING, List, Optional, Union

from vkbottle_types.events.bot_events import MessageEvent

from vkbottle.modules import logger
from vkbottle.tools.event_data import OpenAppEvent, OpenLinkEvent, ShowSnackbarEvent
from vkbottle.tools.formatting import Format, Formatter

if TYPE_CHECKING:
    from vkbottle_types.responses.messages import MessagesSendUserIdsResponseItem

    EventDataType = Union[ShowSnackbarEvent, OpenAppEvent, OpenLinkEvent]
    MessageText = Union[str, Format, Formatter]


class MessageEventMin(MessageEvent):
    @property
    def user_id(self) -> int:
        """alias to event.object.user_id"""

        return self.object.user_id

    @property
    def peer_id(self) -> int:
        """alias to event.object.peer_id"""

        return self.object.peer_id

    @property
    def payload(self) -> Optional[dict]:
        """alias to event.object.payload"""

        return self.object.payload

    @property
    def conversation_message_id(self) -> Optional[int]:
        """alias to event.object.conversation_message_id"""

        return self.object.conversation_message_id

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_id = self.object.event_id

    async def send_message_event_answer(self, event_data: "EventDataType", **kwargs) -> int:
        data = {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "peer_id": self.peer_id,
            "event_data": event_data.model_dump_json(),
        }
        data.update(kwargs)
        return await self.ctx_api.messages.send_message_event_answer(**data)

    async def send_empty_answer(self, **kwargs) -> int:
        data = {
            "event_id": self.event_id,
            "user_id": self.user_id,
            "peer_id": self.peer_id,
        }
        data.update(kwargs)
        return await self.ctx_api.messages.send_message_event_answer(**data)

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
        message: Optional["MessageText"] = None,
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
        if isinstance(message, (Formatter, Format)):
            kwargs["format_data"] = (
                message.raw_format_data
                if isinstance(message, Formatter)
                else message.as_raw_data()
            )

        data = self.ctx_api.messages.get_set_params(locals())
        data["peer_id"] = self.peer_id
        data["conversation_message_id"] = self.conversation_message_id
        return await self.ctx_api.messages.edit(**data)

    async def send_message(
        self,
        message: Optional["MessageText"] = None,
        attachment: Optional[str] = None,
        random_id: Optional[int] = 0,
        lat: Optional[float] = None,
        long: Optional[float] = None,
        reply_to: Optional[int] = None,
        forward_messages: Optional[List[int]] = None,
        forward: Optional[str] = None,
        sticker_id: Optional[int] = None,
        keyboard: Optional[str] = None,
        template: Optional[str] = None,
        payload: Optional[str] = None,
        content_source: Optional[str] = None,
        dont_parse_links: Optional[bool] = None,
        disable_mentions: Optional[bool] = None,
        intent: Optional[str] = None,
        subscribe_id: Optional[int] = None,
        **kwargs,
    ) -> "MessagesSendUserIdsResponseItem":
        if isinstance(message, (Formatter, Format)):
            kwargs["format_data"] = (
                message.raw_format_data
                if isinstance(message, Formatter)
                else message.as_raw_data()
            )

        data = self.ctx_api.messages.get_set_params(locals())
        deprecated_params = ("peer_id", "user_id", "domain", "chat_id", "user_ids")
        deprecated = [k for k in data if k in deprecated_params]
        if deprecated:
            logger.warning(
                "Params like peer_id or user_id is deprecated in MessageEvent.send_message()."
                "Use API.messages.send() instead"
            )
            for k in deprecated:
                data.pop(k, None)

        if message is None:
            message = ""
        elif not isinstance(message, str):
            message = str(message)

        stream = StringIO(message)
        while True:
            if msg := stream.read(4096):
                data["message"] = msg

            response = (await self.ctx_api.messages.send(peer_ids=[self.peer_id], **data))[0]  # type: ignore
            if stream.tell() == len(message or ""):
                break

        return response

    def get_payload_json(self, *args, **kwargs) -> Optional[dict]:
        return self.payload


MessageEventMin.model_rebuild()


__all__ = ("MessageEventMin",)
