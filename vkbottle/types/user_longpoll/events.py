from vkbottle.types.base import BaseModel
import typing


class MessageFields(BaseModel):
    message_id: int
    peer_id: typing.Optional[int] = None
    timestamp: typing.Optional[int] = None
    text: typing.Optional[str] = None
    subject: typing.Optional[str] = None
    info: typing.Optional[str] = None
    attachments: typing.Optional[typing.Union[dict, list]] = None
    random_id: typing.Optional[int] = None


class ReplaceMessageFlags(MessageFields):
    flags: int


class InstallMessageFlags(MessageFields):
    mask: int


class ResetMessageFlags(MessageFields):
    mask: int


class EditMessage(BaseModel):
    message_id: int
    mask: int
    peer_id: int
    timestamp: int
    new_text: str = ""
    attachments: typing.Optional[typing.Union[dict, list]] = None


class InRead(BaseModel):
    peer_id: int
    local_id: int


class OutRead(InRead):
    pass


class FriendOnline(BaseModel):
    user_id: typing.Optional[int] = None
    extra: int = 0
    timestamp: int


class FriendOffline(BaseModel):
    user_id: typing.Optional[int] = None
    flags: int = 0
    timestamp: int


class ResetDialogFlags(BaseModel):
    peer_id: int
    mask: int


class ReplaceDialogFlags(BaseModel):
    peer_id: int
    flags: int


class InstallDialogFlags(ResetDialogFlags):
    pass


class DeleteMessages(InRead):
    pass


class ChangeConversationParams(BaseModel):
    chat_id: int
    self: int


class DialogTypingState(BaseModel):
    user_id: int
    flags: int


class ConversationTypingState(BaseModel):
    user_id: int
    chat_id: int


class Call(BaseModel):
    user_id: int
    call_id: int


class Counter(BaseModel):
    count: int


class ChangedNotificationsSettings(BaseModel):
    peer_id: int
    sound: int
    disabled_until: int


class RestoreDeleted(DeleteMessages):
    pass


class ChatInfoEdit(BaseModel):
    type_id: int
    peer_id: int
    info: typing.Union[str, int]


class ChatVoiceMessageStates(BaseModel):
    user_ids: typing.List[int]
    peer_id: int
    total_count: int
    ts: typing.Optional[int] = None


class ChatEdit(BaseModel):
    chat_id: int = None
    self: int = None
