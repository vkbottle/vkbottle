from typing import Any, Callable, List, Optional, Union

from vkbottle_types import StatePeer
from vkbottle_types.events.bot_events import MessageNew
from vkbottle_types.objects import (
    AudioAudio,
    ClientInfoForBots,
    DocsDoc,
    MessagesMessage,
    PhotosPhoto,
    UsersUser,
    VideoVideo,
    WallWallComment,
    WallWallpostFull,
)

from vkbottle.api import ABCAPI, API


class MessageMin(MessagesMessage):
    group_id: Optional[int] = None
    client_info: Optional["ClientInfoForBots"] = None
    unprepared_ctx_api: Optional[Any] = None
    state_peer: Optional[StatePeer] = None

    @property
    def ctx_api(self) -> Union["ABCAPI", "API"]:
        return getattr(self, "unprepared_ctx_api")

    @property
    def chat_id(self) -> int:
        return self.peer_id - 2_000_000_000

    @property
    def message_id(self) -> int:
        return self.conversation_message_id or self.id

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
        random_id: Optional[int] = 0,
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
        template: Optional[str] = None,
        intent: Optional[str] = None,
        **kwargs,
    ) -> int:
        locals().update(kwargs)
        locals().pop("kwargs")
        data = {k: v for k, v in locals().items() if k != "self" and v is not None}
        data["peer_id"] = self.peer_id

        return (await self.ctx_api.request("messages.send", data))["response"]

    def get_wall_attachment(self) -> List["WallWallpostFull"]:
        result = [attachment.wall for attachment in self.attachments if attachment.wall]
        return result or None

    def get_wall_reply_attachment(self) -> List["WallWallComment"]:
        result = [
            attachment.wall_reply for attachment in self.attachments if attachment.wall_reply
        ]
        return result or None

    def get_photo_attachments(self) -> List["PhotosPhoto"]:
        return [attachment.photo for attachment in self.attachments if attachment.photo]

    def get_video_attachments(self) -> List["VideoVideo"]:
        return [attachment.video for attachment in self.attachments if attachment.video]

    def get_doc_attachments(self) -> List["DocsDoc"]:
        return [attachment.doc for attachment in self.attachments if attachment.doc]

    def get_audio_attachments(self) -> List["AudioAudio"]:
        return [attachment.audio for attachment in self.attachments if attachment.audio]

    def get_message_id(self) -> int:
        return self.id or self.conversation_message_id

    def get_payload_json(
        self,
        throw_error: bool = False,
        unpack_failure: Callable[[str], dict] = lambda payload: payload,
        json: Any = __import__("json"),
    ) -> Union[dict, None]:
        try:
            return json.loads(self.payload)
        except (json.decoder.JSONDecodeError, TypeError) as e:
            if throw_error:
                raise e
        return unpack_failure(self.payload)


MessageMin.update_forward_refs()


def message_min(event: dict, ctx_api: "ABCAPI") -> "MessageMin":
    update = MessageNew(**event)
    message = MessageMin(
        **update.object.message.dict(),
        client_info=update.object.client_info.dict(),
        group_id=update.group_id,
    )
    setattr(message, "unprepared_ctx_api", ctx_api)
    return message
