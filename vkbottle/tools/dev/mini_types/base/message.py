import re
from abc import ABC, abstractmethod
from io import StringIO
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

from pydantic import BaseModel, root_validator
from vkbottle_types.objects import (
    AudioAudio,
    DocsDoc,
    MessagesMessage,
    PhotosPhoto,
    UsersUserFull,
    VideoVideo,
    WallWallComment,
    WallWallpostFull,
)

from vkbottle.dispatch.dispenser.base import StatePeer
from vkbottle.modules import logger

if TYPE_CHECKING:
    from vkbottle_types.responses.messages import MessagesSendUserIdsResponseItem

    from vkbottle.api import ABCAPI, API

MENTION_PATTERN = re.compile(r"^\[(?P<type>club|public|id)(?P<id>\d*)\|(?P<text>.+)\],?\s?")


class Mention(BaseModel):
    """Mention object

    :param id: Identifier of the user that was mentioned (negative if it's a group)
    :param text: Mention text
    """

    id: int
    text: str


class BaseMessageMin(MessagesMessage, ABC):
    unprepared_ctx_api: Optional[Any] = None
    state_peer: Optional["StatePeer"] = None
    _mention: Optional[Mention] = None

    @root_validator
    def __replace_mention(cls, values):
        message_text = values.get("text")
        if not message_text:
            return values
        match = MENTION_PATTERN.search(message_text)
        if not match:
            return values
        values["text"] = message_text.replace(match.group(0), "", 1)
        mention_id = int(match.group("id"))
        if match.group("type") in ("club", "public"):
            mention_id = -mention_id
        values["_mention"] = Mention(id=mention_id, text=match.group("text"))
        return values

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return getattr(self, "unprepared_ctx_api")

    @property
    def mention(self) -> Optional[Mention]:
        """Returns `Mention` object if message contains mention,
        eg if message is `@username text` returns `Mention(id=123, text="text")`,
        also mention is automatically removes from message text"""
        return self._mention

    @property
    @abstractmethod
    def is_mentioned(self) -> bool:
        """Returns True if current bot is mentioned in message"""
        pass

    async def get_user(self, raw_mode: bool = False, **kwargs) -> Union[UsersUserFull, dict]:
        raw_user = (await self.ctx_api.request("users.get", {"user_ids": self.from_id, **kwargs}))[
            "response"
        ][0]
        return raw_user if raw_mode else UsersUserFull(**raw_user)

    @property
    def chat_id(self) -> int:
        return self.peer_id - 2_000_000_000

    @property
    def message_id(self) -> int:
        return self.conversation_message_id or self.id

    def get_wall_attachment(self) -> Optional[List["WallWallpostFull"]]:
        if self.attachments is None:
            return None
        result = [attachment.wall for attachment in self.attachments if attachment.wall]
        return result or None

    def get_wall_reply_attachment(self) -> Optional[List["WallWallComment"]]:
        if self.attachments is None:
            return None
        result = [
            attachment.wall_reply for attachment in self.attachments if attachment.wall_reply
        ]
        return result or None

    def get_photo_attachments(self) -> Optional[List["PhotosPhoto"]]:
        if self.attachments is None:
            return None
        return [attachment.photo for attachment in self.attachments if attachment.photo]

    def get_video_attachments(self) -> Optional[List["VideoVideo"]]:
        if self.attachments is None:
            return None
        return [attachment.video for attachment in self.attachments if attachment.video]

    def get_doc_attachments(self) -> Optional[List["DocsDoc"]]:
        if self.attachments is None:
            return None
        return [attachment.doc for attachment in self.attachments if attachment.doc]

    def get_audio_attachments(self) -> Optional[List["AudioAudio"]]:
        if self.attachments is None:
            return None
        return [attachment.audio for attachment in self.attachments if attachment.audio]

    def get_message_id(self) -> Optional[int]:
        return self.id or self.conversation_message_id

    def get_payload_json(
        self,
        throw_error: bool = False,
        unpack_failure: Callable[[str], Union[dict, str]] = lambda payload: payload,
        json: Any = __import__("json"),
    ) -> Optional[Union[dict, str]]:
        if self.payload is None:
            return None
        try:
            return json.loads(self.payload)
        except (json.decoder.JSONDecodeError, TypeError) as e:
            if throw_error:
                raise e
        return unpack_failure(self.payload)

    async def answer(
        self,
        message: Optional[str] = None,
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
        locals().update(kwargs)

        data = {k: v for k, v in locals().items() if k not in ("self", "kwargs") and v is not None}
        deprecated_params = ("peer_id", "user_id", "domain", "chat_id", "user_ids")
        deprecated = [k for k in data if k in deprecated_params]
        if deprecated:
            logger.warning(
                "Params like peer_id or user_id is deprecated in Message.answer()."
                "Use API.messages.send() instead"
            )
            for k in deprecated:
                data.pop(k)

        stream = StringIO(message)
        while True:
            msg = stream.read(4096)
            if msg:
                data["message"] = msg
            response = (await self.ctx_api.messages.send(peer_ids=[self.peer_id], **data))[0]
            if stream.tell() == len(message or ""):
                break
        return response


BaseMessageMin.update_forward_refs()
