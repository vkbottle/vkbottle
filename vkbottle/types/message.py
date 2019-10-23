import typing
from enum import Enum

from .attachments import Attachment
from .attachments import Geo
from .base import BaseModel
import random


# https://vk.com/dev/objects/message


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


class Message(BaseModel):
    id: int = None
    date: int = None
    peer_id: int = None
    from_id: int = None
    text: str = None
    random_id: int = None
    attachments: typing.List[Attachment] = None
    important: bool = None
    geo: Geo = None
    payload: str = None
    action: MessageAction = None
    fwd_messages: typing.List["Message"] = []
    reply_message: "Message" = None
    api: list = None

    async def reply(
        self,
        message: str = "&#8230;",
        attachment: str = None,
        keyboard: dict = None,
        **params
    ):
        return await self.api[0].request(
            "messages",
            "send",
            dict(
                message=message,
                peer_id=self.peer_id,
                attachment=attachment,
                reply_to=self.id,
                keyboard=keyboard,
                random_id=random.randint(-2e9, 2e9),
                **params
            ),
        )

    async def __call__(
        self,
        message: str = "&#8230;",
        attachment: str = None,
        keyboard: dict = None,
        **params
    ):
        return await self.api[0].request(
            "messages",
            "send",
            dict(
                message=message,
                peer_id=self.peer_id,
                attachment=attachment,
                keyboard=keyboard,
                random_id=random.randint(-2e9, 2e9),
                **params
            ),
        )

    def get_args(self):
        """
        Return message args splitted by whitespace without first (0) element.
        :return: typing.List[str]
        """
        try:
            return self.text.split()[1::]
        except:  # noqa
            return []


Message.update_forward_refs()
