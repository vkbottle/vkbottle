from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union

from pydantic import root_validator
from vkbottle_types.objects import (
    AudioAudio,
    DocsDoc,
    MessagesForeignMessage,
    PhotosPhoto,
    UsersUserFull,
    VideoVideoFull,
    WallWallComment,
    WallWallpostFull,
)

from vkbottle.modules import json, logger

if TYPE_CHECKING:
    from vkbottle.api import ABCAPI, API

from .mention import Mention, replace_mention_validator


class BaseForeignMessageMin(MessagesForeignMessage, ABC):
    unprepared_ctx_api: Optional[Any] = None
    replace_mention: Optional[bool] = None
    _mention: Optional[Mention] = None

    __replace_mention = root_validator(replace_mention_validator, allow_reuse=True, pre=False)  # type: ignore

    class Config:
        frozen = False

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return self.unprepared_ctx_api  # type: ignore

    @property
    def mention(self) -> Optional[Mention]:
        """Returns `Mention` object if message contains mention,
        eg if message is `@username text` returns `Mention(id=123, text="text")`,
        also mention is automatically removes from message text"""
        if not self.replace_mention:
            logger.warning(
                "labeler.message_view.replace_mention is set to False, the mention will not be processed"
            )
            return None
        return self._mention

    @property
    @abstractmethod
    def is_mentioned(self) -> bool:
        """Returns True if current bot is mentioned in message"""

    async def get_user(self, raw_mode: bool = False, **kwargs) -> Union[UsersUserFull, dict]:
        raw_user = (await self.ctx_api.request("users.get", {"user_ids": self.from_id, **kwargs}))[
            "response"
        ][0]
        return raw_user if raw_mode else UsersUserFull(**raw_user)

    @property
    def chat_id(self) -> Optional[int]:
        return None if self.peer_id is None else self.peer_id - 2_000_000_000

    @property
    def message_id(self) -> Optional[int]:
        return self.conversation_message_id or self.id

    def get_attachment_strings(self) -> Optional[List[str]]:
        if self.attachments is None:
            return None
        attachments = []
        for attachment in self.attachments:
            attachment_type = attachment.type.value
            attachment_object = getattr(attachment, attachment_type)
            if not hasattr(attachment_object, "id") or not hasattr(attachment_object, "owner_id"):
                continue
            attachment_string = (
                f"{attachment_type}{attachment_object.owner_id}_{attachment_object.id}"
            )
            if attachment_object.access_key:
                attachment_string += f"_{attachment_object.access_key}"
            attachments.append(attachment_string)
        return attachments

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

    def get_video_attachments(self) -> Optional[List["VideoVideoFull"]]:
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
    ) -> Optional[Union[dict, str]]:
        if self.payload is None:
            return None
        try:
            return json.loads(self.payload)
        except (ValueError, TypeError) as e:
            if throw_error:
                raise e from e
        return unpack_failure(self.payload)


BaseForeignMessageMin.update_forward_refs()
