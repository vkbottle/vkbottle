from . import base, audio, docs, photos, video, gifts, market, wall, users, link, polls
import typing
from enum import Enum
from ..base import BaseModel


class AudioMessage(BaseModel):
    access_key: str = None
    duration: int = None
    id: int = None
    link_mp3: str = None
    link_ogg: str = None
    owner_id: int = None
    waveform: typing.List[int] = None


class Chat(BaseModel):
    admin_id: int = None
    id: int = None
    kicked: "base.BoolInt" = None
    left: "base.BoolInt" = None
    photo_100: str = None
    photo_200: str = None
    photo_50: str = None
    push_settings: "ChatPushSettings" = None
    title: str = None
    type: str = None
    users: typing.List[int] = None


class ChatFull(BaseModel):
    admin_id: int = None
    id: int = None
    kicked: "base.BoolInt" = None
    left: "base.BoolInt" = None
    photo_100: str = None
    photo_200: str = None
    photo_50: str = None
    push_settings: "ChatPushSettings" = None
    title: str = None
    type: str = None
    users: typing.List[int] = None


class ChatPushSettings(BaseModel):
    disabled_until: int = None
    sound: "base.BoolInt" = None


class ChatRestrictions(BaseModel):
    admins_promote_users: bool = None
    only_admins_edit_info: bool = None
    only_admins_edit_pin: bool = None
    only_admins_invite: bool = None
    only_admins_kick: bool = None


class Conversation(BaseModel):
    peer: "ConversationPeer" = None
    last_message_id: int = None
    in_read: int = None
    out_read: int = None
    unread_count: int = None
    important: bool = None
    unanswered: bool = None
    special_service_type: str = None
    message_request: str = None
    mentions: typing.List[int] = None
    current_keyboard: "Keyboard" = None


class ConversationMember(BaseModel):
    can_kick: bool = None
    invited_by: int = None
    is_admin: bool = None
    is_owner: bool = None
    is_message_request: bool = None
    join_date: int = None
    request_date: int = None
    member_id: int = None


class ConversationPeer(BaseModel):
    id: int = None
    local_id: int = None
    type: "ConversationPeerType" = None


class ConversationPeerType(Enum):
    chat = "chat"
    email = "email"
    user = "user"
    group = "group"


class ConversationWithMessage(BaseModel):
    conversation: "Conversation" = None
    last_message: "Message" = None


class ForeignMessage(BaseModel):
    attachments: typing.List["MessageAttachment"] = None
    conversation_message_id: int = None
    date: int = None
    from_id: int = None
    fwd_messages: typing.List["Message"] = None
    geo: "base.Geo" = None
    id: int = None
    peer_id: int = None
    reply_message: "ForeignMessage" = None
    text: str = None
    update_time: int = None


class Graffiti(BaseModel):
    access_key: str = None
    height: int = None
    id: int = None
    owner_id: int = None
    url: str = None
    width: int = None


class HistoryAttachment(BaseModel):
    attachment: "HistoryMessageAttachment" = None
    message_id: int = None
    from_id: int = None


class HistoryMessageAttachment(BaseModel):
    audio: "audio.Audio" = None
    audio_message: "AudioMessage" = None
    doc: "docs.Doc" = None
    graffiti: "Graffiti" = None
    link: "link.Link" = None
    market: "link.Link" = None
    photo: "photos.Photo" = None
    share: "link.Link" = None
    type: "HistoryMessageAttachmentType" = None
    video: "video.Video" = None
    wall: "link.Link" = None
    poll: "polls.Poll" = None


class HistoryMessageAttachmentType(Enum):
    photo = "photo"
    video = "video"
    audio = "audio"
    doc = "doc"
    link = "link"
    market = "market"
    wall = "wall"
    share = "share"
    graffiti = "graffiti"
    audio_message = "audio_message"


class Keyboard(BaseModel):
    author_id: int = None
    buttons: typing.List[dict] = None
    one_time: bool = None
    inline: bool = None


class KeyboardButton(BaseModel):
    action: "KeyboardButtonAction" = None
    color: str = None


class KeyboardButtonAction(BaseModel):
    app_id: int = None
    hash: str = None
    label: str = None
    owner_id: int = None
    payload: str = None
    type: str = None


class LastActivity(BaseModel):
    online: "base.BoolInt" = None
    time: int = None


class LongpollMessages(BaseModel):
    count: int = None
    items: typing.List["Message"] = None


class LongpollParams(BaseModel):
    key: str = None
    pts: int = None
    server: str = None
    ts: int = None


class Message(BaseModel):
    action: "MessageAction" = None
    admin_author_id: int = None
    attachments: typing.List["MessageAttachment"] = None
    conversation_message_id: int = None
    date: int = None
    deleted: "base.BoolInt" = None
    from_id: int = None
    fwd_messages: typing.List["Message"] = None
    geo: "base.Geo" = None
    id: int = None
    important: bool = None
    is_hidden: bool = None
    keyboard: "Keyboard" = None
    members_count: int = None
    out: "base.BoolInt" = None
    payload: str = None
    peer_id: int = None
    random_id: int = None
    ref: str = None
    ref_source: str = None
    reply_message: "ForeignMessage" = None
    text: str = None
    update_time: int = None


class MessageAction(BaseModel):
    conversation_message_id: int = None
    email: str = None
    member_id: int = None
    message: str = None
    photo: "MessageActionPhoto" = None
    text: str = None
    type: "MessageActionStatus" = None


class MessageActionPhoto(BaseModel):
    photo_100: str = None
    photo_200: str = None
    photo_50: str = None


class MessageActionStatus(Enum):
    chat_photo_update = "chat_photo_update"
    chat_photo_remove = "chat_photo_remove"
    chat_create = "chat_create"
    chat_title_update = "chat_title_update"
    chat_invite_user = "chat_invite_user"
    chat_kick_user = "chat_kick_user"
    chat_pin_message = "chat_pin_message"
    chat_unpin_message = "chat_unpin_message"
    chat_invite_user_by_link = "chat_invite_user_by_link"


class MessageAttachment(BaseModel):
    audio: "audio.Audio" = None
    audio_message: "AudioMessage" = None
    doc: "docs.Doc" = None
    poll: "polls.Poll" = None
    gift: "gifts.Layout" = None
    graffiti: "Graffiti" = None
    link: "link.Link" = None
    market: "market.MarketItem" = None
    market_market_album: "market.MarketAlbum" = None
    photo: "photos.Photo" = None
    sticker: "base.Sticker" = None
    type: "MessageAttachmentType" = None
    video: "video.Video" = None
    wall: "wall.WallpostFull" = None
    wall_reply: "wall.WallComment" = None


class MessageAttachmentType(Enum):
    photo = "photo"
    audio = "audio"
    video = "video"
    doc = "doc"
    link = "link"
    poll = "poll"
    market = "market"
    market_album = "market_album"
    gift = "gift"
    sticker = "sticker"
    wall = "wall"
    wall_reply = "wall_reply"
    article = "article"
    graffiti = "graffiti"
    audio_message = "audio_message"


class PinnedMessage(BaseModel):
    attachments: typing.List[MessageAttachment] = None
    conversation_message_id: int = None
    date: int = None
    from_id: int = None
    fwd_messages: typing.List[Message] = None
    geo: "base.Geo" = None
    id: int = None
    peer_id: int = None
    reply_message: "ForeignMessage" = None
    text: str = None
    keyboard: "Keyboard" = None


class UserXtrInvitedBy(users.UserXtrType):
    invited_by: int = None


Message.update_forward_refs()


AudioMessage.update_forward_refs()
Chat.update_forward_refs()
ChatFull.update_forward_refs()
ChatPushSettings.update_forward_refs()
ChatRestrictions.update_forward_refs()
Conversation.update_forward_refs()
ConversationMember.update_forward_refs()
ConversationPeer.update_forward_refs()
ConversationWithMessage.update_forward_refs()
ForeignMessage.update_forward_refs()
Graffiti.update_forward_refs()
HistoryAttachment.update_forward_refs()
HistoryMessageAttachment.update_forward_refs()
Keyboard.update_forward_refs()
KeyboardButton.update_forward_refs()
KeyboardButtonAction.update_forward_refs()
LastActivity.update_forward_refs()
LongpollMessages.update_forward_refs()
LongpollParams.update_forward_refs()
Message.update_forward_refs()
MessageAction.update_forward_refs()
MessageActionPhoto.update_forward_refs()
MessageAttachment.update_forward_refs()
PinnedMessage.update_forward_refs()
UserXtrInvitedBy.update_forward_refs()
