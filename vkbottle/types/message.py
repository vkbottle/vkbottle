import typing
from enum import Enum

from .attachments import Attachment
from .attachments import Geo
from .base import BaseModel
import random
from datetime import datetime


# https://vk.com/dev/objects/message


def sep_bytes(text: str, max_bytes: int = 4096) -> list:
    text = text.encode("utf-8")
    separation = [text[i : i + max_bytes] for i in range(0, len(text), max_bytes)]
    return list(map(bytes.decode, separation)) if len(separation) else [""]


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


class Message(BaseModel):
    id: int = None
    date: int = None
    peer_id: int = None
    from_id: int = None
    text: str = None
    random_id: int = None
    ref: str = None
    ref_source: str = None
    attachments: typing.List[Attachment] = None
    important: bool = None
    geo: Geo = None
    payload: str = None
    keyboard: typing.Union[str, dict] = None
    action: MessageAction = None
    fwd_messages: typing.List["Message"] = []
    reply_message: "Message" = None
    api: list = None
    client_info: "ClientInfo" = None
    conversation_message_id: int = None

    async def reply(
        self,
        message: str = None,
        attachment: str = None,
        keyboard: dict = None,
        **params
    ):
        locals().update(params)
        return await self.api[0].request(
            "messages",
            "send",
            dict(
                peer_id=self.peer_id,
                reply_to=self.id or self.conversation_message_id,
                random_id=random.randint(-2e9, 2e9),
                **{
                    k: v
                    for k, v in locals().items()
                    if v is not None and k not in ["self", "params"]
                }
            ),
        )

    async def __call__(
        self,
        message: str = None,
        attachment: str = None,
        keyboard: dict = None,
        template: dict = None,
        **params
    ):
        locals().update(params)
        for message in sep_bytes(message or ""):
            m = await self.api[0].request(
                "messages",
                "send",
                dict(
                    peer_id=self.peer_id,
                    random_id=random.randint(-2e9, 2e9),
                    **{
                        k: v
                        for k, v in locals().items()
                        if v is not None and k not in ["self", "params"]
                    }
                ),
            )
        return m

    @property
    def date_time(self) -> datetime:
        return datetime.fromtimestamp(self.date)


Message.update_forward_refs()
