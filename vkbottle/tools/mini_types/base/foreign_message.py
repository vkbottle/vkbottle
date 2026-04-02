from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Final

import pydantic
from vkbottle_types.objects import (
    AudioAudio,
    DocsDoc,
    MessagesAudioMessage,
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

PEER_ID_OFFSET: Final[int] = 2_000_000_000


class BaseForeignMessageMin(MessagesForeignMessage, ABC):
    unprepared_ctx_api: Any | None = None
    replace_mention: bool | None = None
    _mention: Mention | None = None
    _is_full: bool | None = None

    model_config = pydantic.ConfigDict(frozen=False)

    @pydantic.model_validator(mode="after")
    def replace_mention_model(self) -> "BaseForeignMessageMin":
        return replace_mention_validator(self)

    @property
    def ctx_api(self) -> "ABCAPI | API":
        if self.unprepared_ctx_api is None:
            raise AssertionError
        return self.unprepared_ctx_api

    @property
    def mention(self) -> Mention | None:
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

    async def get_user(
        self,
        raw_mode: bool = False,
        **kwargs: Any,
    ) -> UsersUserFull | dict[str, Any]:
        raw_user = (await self.ctx_api.request("users.get", {"user_ids": self.from_id, **kwargs}))[
            "response"
        ][0]
        return raw_user if raw_mode else UsersUserFull(**raw_user)

    async def get_full_message(self, peer_id: int | None = None) -> "BaseForeignMessageMin":
        peer_id = peer_id or self.peer_id

        if self._is_full or peer_id is None:
            return self

        message = (
            await self.ctx_api.messages.get_by_conversation_message_id(
                peer_id=peer_id,
                conversation_message_ids=[self.conversation_message_id],
            )
        ).items[0]

        self.__dict__.update(message.__dict__)
        super().__init__(**self.model_dump())
        self.__dict__["_is_full"] = True

        return self

    @property
    def chat_id(self) -> int | None:
        return None if self.peer_id is None else self.peer_id - PEER_ID_OFFSET

    @property
    def message_id(self) -> int | None:
        return self.conversation_message_id or self.id

    def get_attachment_strings(self) -> list[str] | None:
        if self.attachments is None:
            return None

        attachments = []
        for attachment in self.attachments:
            attachment_type = attachment.type.value
            attachment_object = getattr(attachment, attachment_type)
            if not hasattr(attachment_object, "id") or not hasattr(attachment_object, "owner_id"):
                logger.debug("Got unsupported attachment type: {}", attachment_type)
                continue

            attachment_string = (
                f"{attachment_type}{attachment_object.owner_id}_{attachment_object.id}"
            )
            if hasattr(attachment_object, "access_key"):
                attachment_string += f"_{attachment_object.access_key}"

            attachments.append(attachment_string)

        return attachments

    def get_wall_attachment(self) -> list["WallWallpostFull"] | None:
        if self.attachments is None:
            return None
        result = [attachment.wall for attachment in self.attachments if attachment.wall]  # type: ignore
        return result or None

    def get_wall_reply_attachment(self) -> list["WallWallComment"] | None:
        if self.attachments is None:
            return None
        result = [
            attachment.wall_reply for attachment in self.attachments if attachment.wall_reply
        ]
        return result or None

    def get_photo_attachments(self) -> list["PhotosPhoto"] | None:
        if self.attachments is None:
            return None
        return [attachment.photo for attachment in self.attachments if attachment.photo]

    def get_video_attachments(self) -> list["VideoVideoFull"] | None:
        if self.attachments is None:
            return None
        return [attachment.video for attachment in self.attachments if attachment.video]  # type: ignore

    def get_doc_attachments(self) -> list["DocsDoc"] | None:
        if self.attachments is None:
            return None
        return [attachment.doc for attachment in self.attachments if attachment.doc]

    def get_audio_attachments(self) -> list["AudioAudio"] | None:
        if self.attachments is None:
            return None
        return [attachment.audio for attachment in self.attachments if attachment.audio]

    def get_audio_message_attachments(self) -> list["MessagesAudioMessage"] | None:
        if self.attachments is None:
            return None
        return [
            attachment.audio_message for attachment in self.attachments if attachment.audio_message
        ]

    def get_message_id(self) -> int | None:
        return self.id or self.conversation_message_id

    def get_payload_json(
        self,
        throw_error: bool = False,
        unpack_failure: Callable[[str], dict[str, Any] | str] = lambda payload: payload,
    ) -> dict[str, Any] | str | None:
        if self.payload is None:
            return None

        try:
            return json.loads(self.payload)
        except (ValueError, TypeError) as e:
            if throw_error:
                raise e from None

        return unpack_failure(self.payload)


BaseForeignMessageMin.object_build(locals())


__all__ = ("BaseForeignMessageMin",)
