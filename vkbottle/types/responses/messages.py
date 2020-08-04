import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class SetChatPhoto(BaseModel):
    message_id: int = None
    chat: objects.messages.Chat = None


class SetChatPhotoModel(BaseModel):
    response: SetChatPhoto = None


CreateChat = int


class CreateChatModel(BaseModel):
    response: CreateChat = None


class DeleteChatPhoto(BaseModel):
    message_id: int = None
    chat: objects.messages.Chat = None


class DeleteChatPhotoModel(BaseModel):
    response: DeleteChatPhoto = None


class DeleteConversation(BaseModel):
    last_deleted_id: int = None


class DeleteConversationModel(BaseModel):
    response: DeleteConversation = None


Edit = objects.base.BoolInt


class EditModel(BaseModel):
    response: Edit = None


class GetByConversationMessageId(BaseModel):
    count: int = None
    items: typing.List[objects.messages.Message] = None


class GetByConversationMessageIdModel(BaseModel):
    response: GetByConversationMessageId = None


class GetById(BaseModel):
    count: int = None
    items: typing.List[objects.messages.Message] = None


class GetByIdModel(BaseModel):
    response: GetById = None


class GetChatPreview(BaseModel):
    preview: dict = None
    profiles: typing.List[objects.message.ChatPreview] = None


class GetChatPreviewModel(BaseModel):
    response: GetChatPreview = None


GetChat = objects.messages.Chat


class GetChatModel(BaseModel):
    response: GetChat = None


class GetConversationMembers(BaseModel):
    count: int = None
    items: typing.List["objects.messages.ConversationMember"] = None
    chat_restrictions: objects.messages.ChatRestrictions = None
    profiles: typing.List["objects.users.User"] = None
    groups: typing.List["objects.groups.Group"] = None


class GetConversationMembersModel(BaseModel):
    response: GetConversationMembers = None


class GetConversationsById(BaseModel):
    count: int = None
    items: typing.List["Conversation"] = None


class GetConversationsByIdModel(BaseModel):
    response: GetConversationsById = None


class ConversationType(enum.Enum):
    chat = "chat"
    user = "user"
    group = "group"
    email = "email"


class Peer(BaseModel):
    id: int = None
    type: ConversationType = None
    local_id: int = None


class PushSettings(BaseModel):
    disabled_until: int = None
    disabled_forever: bool = None
    no_sound: bool = None


class CanWrite(BaseModel):
    allowed: bool = None
    reason: int = None

    def get_reason(self) -> str:
        return {
            18: "the user is deleted or blocked",
            900: "can't send message to user from blacklist",
            901: "the user has denied messages from the community",
            902: "the user has closed messages using privacy settings",
            915: "messages are disabled in the community",
            916: "messages are blocked in the community",
            917: "no access to conversation;",
            918: "no access to e-mail",
            203: "no access to the community",
        }.get(self.reason, f"unknown reason {self.reason}")


class ConversationUserState(enum.Enum):
    in_ = "in"
    kicked = "kicked"
    left = "left"


class ChatSettings(BaseModel):
    members_count: int = None
    title: str = None
    pinned_message: objects.messages.Message = None
    state: ConversationUserState = None
    photo: objects.photos.PhotoSizes = None
    admin_ids: typing.List[int] = None
    owner_id: int = None
    active_ids: typing.List[int] = None


class Conversation(BaseModel):
    peer: Peer = None
    in_read: int = None
    out_read: int = None
    unread_count: int = None
    important: bool = None
    unanswered: bool = None
    push_settings: PushSettings = None
    can_write: CanWrite = None
    chat_settings: ChatSettings = None


class ConversationsItem(BaseModel):
    conversation: Conversation = None
    last_message: objects.messages.Message = None


class GetConversations(BaseModel):
    count: int = None
    unread_count: int = None
    items: typing.List[ConversationsItem] = None
    profiles: typing.List[objects.users.User] = None
    groups: typing.List[objects.groups.Group] = None


class GetConversationsModel(BaseModel):
    response: GetConversations = None


class GetHistoryAttachments(BaseModel):
    items: typing.List[objects.messages.HistoryAttachment] = None
    next_from: str = None


class GetHistoryAttachmentsModel(BaseModel):
    response: GetHistoryAttachments = None


class GetHistory(BaseModel):
    count: int = None
    items: typing.List[objects.messages.Message] = None
    in_read: int = None
    out_read: int = None


class GetHistoryModel(BaseModel):
    response: GetHistory = None


class GetInviteLink(BaseModel):
    link: str = None


class GetInviteLinkModel(BaseModel):
    response: GetInviteLink = None


GetLastActivity = objects.messages.LastActivity


class GetLastActivityModel(BaseModel):
    response: GetLastActivity = None


class GetLongPollHistory(BaseModel):
    history: typing.List[typing.List[int]] = None
    groups: typing.List[objects.groups.Group] = None
    messages: objects.messages.LongpollMessages = None
    profiles: typing.List[objects.users.User] = None
    new_pts: int = None
    more: bool = None


class GetLongPollHistoryModel(BaseModel):
    response: GetLongPollHistory = None


GetLongPollServer = objects.messages.LongpollParams


class GetLongPollServerModel(BaseModel):
    response: GetLongPollServer = None


class IsMessagesFromGroupAllowed(BaseModel):
    is_allowed: int = None


class IsMessagesFromGroupAllowedModel(BaseModel):
    response: IsMessagesFromGroupAllowed = None


class JoinChatByInviteLink(BaseModel):
    chat_id: int = None


class JoinChatByInviteLinkModel(BaseModel):
    response: JoinChatByInviteLink = None


MarkAsImportant = typing.List[int]


class MarkAsImportantModel(BaseModel):
    response: MarkAsImportant = None


Pin = objects.messages.PinnedMessage


class PinModel(BaseModel):
    response: Pin = None


class SearchConversations(BaseModel):
    count: int = None
    items: typing.List[objects.messages.Conversation] = None
    profiles: typing.List[objects.users.User] = None
    groups: typing.List[objects.groups.Group] = None


class SearchConversationsModel(BaseModel):
    response: SearchConversations = None


class Search(BaseModel):
    count: int = None
    items: typing.List[objects.messages.Message] = None


class SearchModel(BaseModel):
    response: Search = None


Send = int


class SendModel(BaseModel):
    response: typing.Union[Send, typing.List[objects.messages.Message]] = None


GetConversationsById.update_forward_refs()
