import typing
from enum import Enum

from .attachments import Attachment
from .attachments import Geo
from .base import BaseModel
from vkbottle.api import Api
from datetime import datetime
from vkbottle.framework.framework import FromExtension

# https://vk.com/dev/objects/message

def sep_bytes(text: str, max_bytes: int = 4096) -> list:
    text = text.encode("utf-8")
    separation = [text[i:i + max_bytes] for i in range(0, len(text), max_bytes)]
    return list(map(bytes.decode, separation)) if len(separation) else [""]


class GetApi:
    @property
    def api(self) -> Api:
        return Api.get_current()


class Action(Enum):
    chat_photo_update = "chat_photo_update"
    chat_photo_remove = "chat_photo_remove"
    chat_create = "chat_create"
    chat_title_update = "chat_title_update"
    chat_invite_user = "chat_invite_user"
    chat_kick_user = "chat_kick_user"
    chat_pin_message = "chat_pin_message"
    chat_unpin_message = "chat_unpin_message"
    chat_invite_user_by_link = "chat_invite_user_by_link"


class MessageActionPhoto(BaseModel):
    photo_50: str = None
    photo_100: str = None
    photo_200: str = None


class MessageAction(BaseModel):
    type: Action = None
    member_id: int = None
    text: str = None
    email: str = None
    photo: MessageActionPhoto = None


class ClientInfo(BaseModel):
    button_actions: list = None
    keyboard: bool = None
    inline_keyboard: bool = None
    carousel: bool = None
    lang_id: int = None


class Message(BaseModel, GetApi):
    id: int = None
    date: int = None
    peer_id: int = None
    from_id: int = None
    text: str = None
    random_id: int = None
    ref: str = None
    ref_source: str = None
    attachments: typing.List[Attachment] = []
    important: bool = None
    geo: Geo = None
    payload: str = None
    keyboard: typing.Union[str, dict] = None
    action: MessageAction = None
    fwd_messages: typing.List["Message"] = []
    reply_message: "Message" = None
    client_info: ClientInfo = None
    conversation_message_id: int = None

    @property
    def chat_id(self) -> int:
        return self.peer_id - 2000000000

    async def reply(
            self,
            message: str = None,
            attachment: str = None,
            user_id: int = None,
            domain: str = None,
            chat_id: int = None,
            random_id: int = FromExtension("random_id"),
            user_ids: typing.List[int] = None,
            lat: typing.Any = None,
            long: typing.Any = None,
            forward_messages: typing.List[int] = None,
            forward: str = None,
            sticker_id: int = None,
            group_id: int = None,
            keyboard: str = None,
            payload: str = None,
            dont_parse_links: bool = None,
            disable_mentions: bool = None,
        ):

        if message is not None:
            message = str(message)

        return self.api.messages.send(
            **self.get_params(locals()),
            reply_to=self.id or self.conversation_message_id,
            peer_id=self.peer_id,
        )

    async def __call__(
            self,
            message: str = None,
            attachment: str = None,
            user_id: int = None,
            domain: str = None,
            chat_id: int = None,
            random_id: int = FromExtension("random_id"),
            user_ids: typing.List[int] = None,
            lat: typing.Any = None,
            long: typing.Any = None,
            reply_to: int = None,
            forward_messages: typing.List[int] = None,
            forward: str = None,
            sticker_id: int = None,
            group_id: int = None,
            keyboard: str = None,
            payload: str = None,
            dont_parse_links: bool = None,
            disable_mentions: bool = None,
    ):
        if not message:
            return await self.api.messages.send(
                **self.get_params(locals()),
                peer_id=self.peer_id,
            )
        _m = []
        for message in sep_bytes(str(message if message is not None else "")):
            _mid = await self.api.messages.send(
                **self.get_params(locals()),
                peer_id=self.peer_id,
            )
            _m.append(_mid)
        return _m if len(_m) > 1 else _m[0]

    @property
    def date_time(self) -> datetime:
        return datetime.fromtimestamp(self.date)


Message.update_forward_refs()
