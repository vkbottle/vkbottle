from .others import SimpleResponse
from ..base import BaseModel
from ..chat import Chat
from ..message import Message
from ..community import Community
from ..additional import Email
from ..user import User
from ..attachments import Photo
from ..conversation import Conversation

from typing import List, Any


class AddChatUser(SimpleResponse):
    pass


class AllowMessagesFromGroup(SimpleResponse):
    pass


class CreateChat(SimpleResponse):
    pass


class Delete(SimpleResponse):
    pass


class DeleteChatPhotoResponse(BaseModel):
    message_id: int = None
    chat: Chat = None


class DeleteChatPhoto(BaseModel):
    response: DeleteChatPhotoResponse = None


class DeleteConversation(SimpleResponse):
    pass


class DenyMessagesFromGroup(SimpleResponse):
    pass


class Edit(SimpleResponse):
    pass


class EditChat(SimpleResponse):
    pass


class GetByConversationMessageIdResponse(BaseModel):
    count: int = None
    items: List[Message] = []


class GetByConversationMessageId(BaseModel):
    response: GetByConversationMessageIdResponse = None


class GetById(BaseModel):
    response: GetByConversationMessageIdResponse = None


class GetChat(BaseModel):
    response: Chat = None


class ChatMembers(BaseModel):
    profiles: List[User] = []
    groups: List[Community] = []
    email: List[Email] = []


class GetChatPreviewResponse(BaseModel):
    admin_id: int = None
    members: ChatMembers = None
    title: str = None
    photo: Photo


class GetChatPreview(BaseModel):
    response: GetChatPreviewResponse = None


class GetConversationMembersResponseItem(BaseModel):
    member_id: int = None
    invited_by: int = None
    join_date: int = None
    is_admin: bool = None


class GetConversationMembersResponse(BaseModel):
    count: int = None
    items: List[GetConversationMembersResponseItem] = []
    profiles: List[User] = []
    groups: List[Community] = []


class GetConverationMembers(BaseModel):
    response: GetConversationMembersResponse = None


class GetConversationsResponse(BaseModel):
    count: int = None
    items: Any = None
    unread_count: int = None
    profiles: List[User] = []
    groups: List[Community] = []


class GetConversations(BaseModel):
    response: GetConversationsResponse = None


class GetConversationsByIdResponse(BaseModel):
    count: int = None
    items: List[Conversation] = []


class GetConversationsById(BaseModel):
    response: GetConversationsByIdResponse = None


class GetHistoryResponse(BaseModel):
    count: int = None
    items: List[Message] = []


class GetHistory(BaseModel):
    response: GetHistoryResponse = None


class GetHistoryAttachments(BaseModel):
    response: Any = []


class GetImportantMessagesResponseMessages(BaseModel):
    count: int = None
    items: List[Message] = []


class GetImportantMessagesResponse(BaseModel):
    messages: GetImportantMessagesResponseMessages = None


class GetImportantMessages(BaseModel):
    response: GetImportantMessagesResponse = None


class GetInviteLinkResponse(BaseModel):
    link: str = None


class GetInviteLink(BaseModel):
    response: GetInviteLinkResponse = None


class GetLastActivityResponse(BaseModel):
    online: int = None
    time: int = None


class GetLastActivity(BaseModel):
    response: GetLastActivityResponse = None


class GetLongPollHistoryResponse(BaseModel):
    history: List[List[int]] = []
    messages: GetImportantMessagesResponseMessages = None
    profiles: List[User] = []
    new_pts: int = None


class GetLongPollHistory(BaseModel):
    response: GetLongPollHistoryResponse = None


class GetLongPollServerResponse(BaseModel):
    key: str = None
    server: str = None
    ts: int = None


class GetLongPollServer(BaseModel):
    response: GetLongPollServerResponse = None


class IsMessagesFromGroupAllowedResponse(BaseModel):
    is_allowed: int = None


class IsMessagesFromGroupAllowed(BaseModel):
    response: IsMessagesFromGroupAllowedResponse = None


class JoinChatByInviteLinkResponse(BaseModel):
    chat_id: int = None


class JoinChatByInviteLink(BaseModel):
    response: JoinChatByInviteLinkResponse = None


class MarkAsAnsweredConversation(SimpleResponse):
    pass


class MarkAsImportant(BaseModel):
    response: List[int] = []


class MarkAsImportantConversation(SimpleResponse):
    pass


class MarkAsRead(SimpleResponse):
    pass


class Pin(SimpleResponse):
    pass


class RemoveChatUser(SimpleResponse):
    pass


class Restore(SimpleResponse):
    pass


class SearchResponse(BaseModel):
    count: int = None
    items: List[Message] = []


class Search(BaseModel):
    response: SearchResponse = None


class SeacrhConversationsResponse(BaseModel):
    count: int = None
    items: List[Conversation] = []


class SearchConversations(BaseModel):
    response: SeacrhConversationsResponse = None


class Send(SimpleResponse):
    pass


class SetActivity(SimpleResponse):
    pass


class SetChatPhotoResponse(BaseModel):
    message_id: int = None
    chat: Chat = None


class SetChatPhoto(BaseModel):
    response: SetChatPhotoResponse = None


class Unpin(SimpleResponse):
    pass
