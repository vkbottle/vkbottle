from . import base, market, users
import typing
from enum import Enum
from ..base import BaseModel


class Address(BaseModel):
    additional_address: str = None
    address: str = None
    city_id: int = None
    country_id: int = None
    distance: int = None
    id: int = None
    latitude: float = None
    longitude: float = None
    metro_station_id: int = None
    phone: str = None
    time_offset: int = None
    timetable: "AddressTimetable" = None
    title: str = None
    work_info_status: "AddressWorkInfoStatus" = None


class AddressTimetable(BaseModel):
    fri: "AddressTimetableDay" = None
    mon: "AddressTimetableDay" = None
    sat: "AddressTimetableDay" = None
    sun: "AddressTimetableDay" = None
    thu: "AddressTimetableDay" = None
    tue: "AddressTimetableDay" = None
    wed: "AddressTimetableDay" = None


class AddressTimetableDay(BaseModel):
    break_close_time: int = None
    break_open_time: int = None
    close_time: int = None
    open_time: int = None


class AddressWorkInfoStatus(Enum):
    no_information = "no_information"
    temporarily_closed = "temporarily_closed"
    always_opened = "always_opened"
    timetable = "timetable"
    forever_closed = "forever_closed"


class AddressesInfo(BaseModel):
    is_enabled: bool = None
    main_address_id: int = None


class BanInfo(BaseModel):
    admin_id: int = None
    comment: str = None
    comment_visible: bool = None
    is_closed: bool = None
    date: int = None
    end_date: int = None
    reason: int = None


class CallbackServer(BaseModel):
    id: int = None
    title: str = None
    creator_id: int = None
    url: str = None
    secret_key: str = None
    status: str = None


class CallbackSettings(BaseModel):
    api_version: str = None
    events: "LongPollEvents" = None


class ContactsItem(BaseModel):
    desc: str = None
    email: str = None
    phone: str = None
    user_id: int = None


class CountersGroup(BaseModel):
    addresses: int = None
    albums: int = None
    audios: int = None
    docs: int = None
    market: int = None
    photos: int = None
    topics: int = None
    videos: int = None


class Cover(BaseModel):
    enabled: "base.BoolInt" = None
    images: typing.List = None


class Fields(Enum):
    market = "market"
    member_status = "member_status"
    is_favorite = "is_favorite"
    is_subscribed = "is_subscribed"
    city = "city"
    country = "country"
    verified = "verified"
    description = "description"
    wiki_page = "wiki_page"
    members_count = "members_count"
    counters = "counters"
    cover = "cover"
    can_post = "can_post"
    can_see_all_posts = "can_see_all_posts"
    activity = "activity"
    fixed_post = "fixed_post"
    can_create_topic = "can_create_topic"
    can_upload_video = "can_upload_video"
    has_photo = "has_photo"
    status = "status"
    main_album_id = "main_album_id"
    links = "links"
    contacts = "contacts"
    site = "site"
    main_section = "main_section"
    trending = "trending"
    can_message = "can_message"
    is_market_cart_enabled = "is_market_cart_enabled"
    is_messages_blocked = "is_messages_blocked"
    can_send_notify = "can_send_notify"
    online_status = "online_status"
    start_date = "start_date"
    finish_date = "finish_date"
    age_limits = "age_limits"
    ban_info = "ban_info"
    action_button = "action_button"
    author_id = "author_id"
    phone = "phone"
    has_market_app = "has_market_app"
    addresses = "addresses"
    live_covers = "live_covers"
    is_adult = "is_adult"
    can_subscribe_posts = "can_subscribe_posts"
    warning_notification = "warning_notification"


class Filter(Enum):
    admin = "admin"
    editor = "editor"
    moder = "moder"
    groups = "groups"
    publics = "publics"
    events = "events"
    has_addresses = "has_addresses"


class Group(BaseModel):
    admin_level: int = None
    deactivated: str = None
    finish_date: int = None
    id: int = None
    wall: int = None
    is_admin: "base.BoolInt" = None
    is_advertiser: "base.BoolInt" = None
    is_closed: int = None
    is_member: "base.BoolInt" = None
    name: str = None
    photo_100: str = None
    photo_200: str = None
    photo_50: str = None
    screen_name: str = None
    start_date: int = None
    type: "GroupType" = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class GroupBanInfo(BaseModel):
    type: str = None
    group: Group = None
    profile: users.User = None
    ban_info: BanInfo = None


class GroupCategory(BaseModel):
    id: int = None
    name: str = None
    subcategories: typing.List = None


class GroupCategoryFull(BaseModel):
    id: int = None
    name: str = None
    page_count: int = None
    page_previews: typing.List = None
    subcategories: typing.List = None


class GroupCategoryType(BaseModel):
    id: int = None
    name: str = None


class GroupFull(Group):
    market: "MarketInfo" = None
    member_status: int = None
    is_favorite: "base.BoolInt" = None
    is_subscribed: "base.BoolInt" = None
    city: "base.Object" = None
    country: "base.Country" = None
    verified: "base.BoolInt" = None
    description: str = None
    wiki_page: str = None
    members_count: int = None
    counters: "CountersGroup" = None
    cover: "Cover" = None
    can_post: "base.BoolInt" = None
    can_see_all_posts: "base.BoolInt" = None
    activity: str = None
    fixed_post: int = None
    can_create_topic: "base.BoolInt" = None
    can_upload_video: "base.BoolInt" = None
    has_photo: "base.BoolInt" = None
    status: str = None
    main_album_id: int = None
    links: typing.List = None
    contacts: typing.List = None
    site: str = None
    main_section: int = None
    trending: "base.BoolInt" = None
    can_message: "base.BoolInt" = None
    is_messages_blocked: "base.BoolInt" = None
    can_send_notify: "base.BoolInt" = None
    online_status: "OnlineStatus" = None
    age_limits: int = None
    ban_info: "GroupBanInfo" = None
    addresses: "AddressesInfo" = None
    is_subscribed_podcasts: bool = None
    can_subscribe_podcasts: bool = None
    can_subscribe_posts: bool = None


class GroupLink(BaseModel):
    name: str = None
    desc: str = None
    edit_title: "base.BoolInt" = None
    id: int = None
    image_processing: "base.BoolInt" = None
    url: str = None


class GroupPublicCategoryList(BaseModel):
    id: int = None
    name: str = None
    subtypes_list: typing.List = None


class GroupRole(Enum):
    moderator = "moderator"
    editor = "editor"
    administrator = "administrator"


class GroupSettings(BaseModel):
    access: int = None
    address: str = None
    audio: int = None
    description: str = None
    docs: int = None
    obscene_filter: "base.BoolInt" = None
    obscene_stopwords: "base.BoolInt" = None
    obscene_words: str = None
    photos: int = None
    public_category: int = None
    public_category_list: typing.List = None
    public_subcategory: int = None
    rss: str = None
    subject: int = None
    subject_list: typing.List = None
    title: str = None
    topics: int = None
    video: int = None
    wall: int = None
    website: str = None
    wiki: int = None


class GroupType(Enum):
    group = "group"
    page = "page"
    event = "event"


class GroupXtrInvitedBy(BaseModel):
    admin_level: int = None
    id: str = None
    invited_by: int = None
    is_admin: "base.BoolInt" = None
    is_advertiser: "base.BoolInt" = None
    is_closed: "base.BoolInt" = None
    is_member: "base.BoolInt" = None
    name: str = None
    photo_100: str = None
    photo_200: str = None
    photo_50: str = None
    screen_name: str = None
    type: "GroupXtrInvitedByType" = None


class GroupXtrInvitedByType(Enum):
    group = "group"
    page = "page"
    event = "event"


class GroupsArray(BaseModel):
    count: int = None
    items: typing.List = None


class LinksItem(BaseModel):
    desc: str = None
    edit_title: "base.BoolInt" = None
    id: int = None
    name: str = None
    photo_100: str = None
    photo_50: str = None
    url: str = None


class LongPollEvents(BaseModel):
    audio_new: "base.BoolInt" = None
    board_post_delete: "base.BoolInt" = None
    board_post_edit: "base.BoolInt" = None
    board_post_new: "base.BoolInt" = None
    board_post_restore: "base.BoolInt" = None
    group_change_photo: "base.BoolInt" = None
    group_change_settings: "base.BoolInt" = None
    group_join: "base.BoolInt" = None
    group_leave: "base.BoolInt" = None
    group_officers_edit: "base.BoolInt" = None
    lead_forms_new: "base.BoolInt" = None
    market_comment_delete: "base.BoolInt" = None
    market_comment_edit: "base.BoolInt" = None
    market_comment_new: "base.BoolInt" = None
    market_comment_restore: "base.BoolInt" = None
    message_allow: "base.BoolInt" = None
    message_deny: "base.BoolInt" = None
    message_new: "base.BoolInt" = None
    message_read: "base.BoolInt" = None
    message_reply: "base.BoolInt" = None
    message_typing_state: "base.BoolInt" = None
    messages_edit: "base.BoolInt" = None
    photo_comment_delete: "base.BoolInt" = None
    photo_comment_edit: "base.BoolInt" = None
    photo_comment_new: "base.BoolInt" = None
    photo_comment_restore: "base.BoolInt" = None
    photo_new: "base.BoolInt" = None
    poll_vote_new: "base.BoolInt" = None
    user_block: "base.BoolInt" = None
    user_unblock: "base.BoolInt" = None
    video_comment_delete: "base.BoolInt" = None
    video_comment_edit: "base.BoolInt" = None
    video_comment_new: "base.BoolInt" = None
    video_comment_restore: "base.BoolInt" = None
    video_new: "base.BoolInt" = None
    wall_post_new: "base.BoolInt" = None
    wall_reply_delete: "base.BoolInt" = None
    wall_reply_edit: "base.BoolInt" = None
    wall_reply_new: "base.BoolInt" = None
    wall_reply_restore: "base.BoolInt" = None
    wall_repost: "base.BoolInt" = None


class LongPollServer(BaseModel):
    key: str = None
    server: str = None
    ts: str = None


class LongPollSettings(BaseModel):
    api_version: str = None
    events: "LongPollEvents" = None
    is_enabled: bool = None


class MarketInfo(BaseModel):
    contact_id: int = None
    currency: "market.Currency" = None
    currency_text: str = None
    enabled: "base.BoolInt" = None
    main_album_id: int = None
    price_max: int = None
    price_min: int = None


class MemberRole(BaseModel):
    id: int = None
    permissions: typing.List = None
    role: "MemberRoleStatus" = None


class MemberRolePermission(Enum):
    ads = "ads"


class MemberRoleStatus(Enum):
    moderator = "moderator"
    editor = "editor"
    administrator = "administrator"
    creator = "creator"


class MemberStatus(BaseModel):
    member: "base.BoolInt" = None
    user_id: int = None


class MemberStatusFull(BaseModel):
    can_invite: "base.BoolInt" = None
    can_recall: "base.BoolInt" = None
    invitation: "base.BoolInt" = None
    member: "base.BoolInt" = None
    request: "base.BoolInt" = None
    user_id: int = None


class OnlineStatus(BaseModel):
    minutes: int = None
    status: "OnlineStatusType" = None


class OnlineStatusType(Enum):
    none = "none"
    online = "online"
    answer_mark = "answer_mark"


class OwnerXtrBanInfo(BaseModel):
    ban_info: "BanInfo" = None
    group: "Group" = None
    profile: "users.User" = None
    type: "OwnerXtrBanInfoType" = None


class OwnerXtrBanInfoType(Enum):
    group = "group"
    profile = "profile"


class RoleOptions(Enum):
    moderator = "moderator"
    editor = "editor"
    administrator = "administrator"
    creator = "creator"


class SubjectItem(BaseModel):
    id: int = None
    name: str = None


class TokenPermissionSetting(BaseModel):
    name: str = None
    setting: int = None


class UserXtrRole(users.UserFull):
    role: "RoleOptions" = None


Address.update_forward_refs()
AddressTimetable.update_forward_refs()
AddressTimetableDay.update_forward_refs()
AddressesInfo.update_forward_refs()
BanInfo.update_forward_refs()
CallbackServer.update_forward_refs()
CallbackSettings.update_forward_refs()
ContactsItem.update_forward_refs()
CountersGroup.update_forward_refs()
Cover.update_forward_refs()
Group.update_forward_refs()
GroupBanInfo.update_forward_refs()
GroupCategory.update_forward_refs()
GroupCategoryFull.update_forward_refs()
GroupCategoryType.update_forward_refs()
GroupFull.update_forward_refs()
GroupLink.update_forward_refs()
GroupPublicCategoryList.update_forward_refs()
GroupSettings.update_forward_refs()
GroupXtrInvitedBy.update_forward_refs()
GroupsArray.update_forward_refs()
LinksItem.update_forward_refs()
LongPollEvents.update_forward_refs()
LongPollServer.update_forward_refs()
LongPollSettings.update_forward_refs()
MarketInfo.update_forward_refs()
MemberRole.update_forward_refs()
MemberStatus.update_forward_refs()
MemberStatusFull.update_forward_refs()
OnlineStatus.update_forward_refs()
OwnerXtrBanInfo.update_forward_refs()
SubjectItem.update_forward_refs()
TokenPermissionSetting.update_forward_refs()
UserXtrRole.update_forward_refs()
