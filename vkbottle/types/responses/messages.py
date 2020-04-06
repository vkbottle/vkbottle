import typing
import enum
from ..base import BaseModel
from vkbottle.types import objects


class SetChatPhoto(BaseModel):
    message_id: int = None
    chat: objects.messages.Chat = None


class SetChatPhotoModel(BaseModel):
    response: SetChatPhoto = None


CreateChat = typing.Dict


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
    items: typing.List = None


class GetByConversationMessageIdModel(BaseModel):
    response: GetByConversationMessageId = None


class GetById(BaseModel):
    count: int = None
    items: typing.List = None


class GetByIdModel(BaseModel):
    response: GetById = None


class GetChatPreview(BaseModel):
    preview: dict = None
    profiles: typing.List = None


class GetChatPreviewModel(BaseModel):
    response: GetChatPreview = None


GetChat = objects.messages.Chat


class GetChatModel(BaseModel):
    response: GetChat = None


class GetConversationMembers(BaseModel):
    count: int = None
    items: typing.List = None
    chat_restrictions: objects.messages.ChatRestrictions = None
    profiles: typing.List = None
    groups: typing.List = None


class GetConversationMembersModel(BaseModel):
    response: GetConversationMembers = None


class GetConversationsById(BaseModel):
    count: int = None
    items: typing.List = None


class GetConversationsByIdModel(BaseModel):
    response: GetConversationsById = None


class GetConversations(BaseModel):
    count: int = None
    unread_count: int = None
    items: typing.List = None
    profiles: typing.List = None
    groups: typing.List = None


class GetConversationsModel(BaseModel):
    response: GetConversations = None


class GetHistoryAttachments(BaseModel):
    items: typing.List = None
    next_from: str = None


class GetHistoryAttachmentsModel(BaseModel):
    response: GetHistoryAttachments = None


class GetHistory(BaseModel):
    count: int = None
    items: typing.List = None
    profiles: typing.List = None
    groups: typing.List = None


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
    history: typing.List = None
    groups: typing.List = None
    messages: objects.messages.LongpollMessages = None
    profiles: typing.List = None
    chats: typing.List = None
    new_pts: int = None
    more: bool = None
    conversations: typing.List = None


class GetLongPollHistoryModel(BaseModel):
    response: GetLongPollHistory = None


GetLongPollServer = objects.messages.LongpollParams


class GetLongPollServerModel(BaseModel):
    response: GetLongPollServer = None


class IsMessagesFromGroupAllowed(BaseModel):
    is_allowed: objects.base.BoolInt = None


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
    items: typing.List = None
    profiles: typing.List = None
    groups: typing.List = None


class SearchConversationsModel(BaseModel):
    response: SearchConversations = None


class Search(BaseModel):
    count: int = None
    items: typing.List = None


class SearchModel(BaseModel):
    response: Search = None


Send = typing.Dict


class SendModel(BaseModel):
    response: Send = None
