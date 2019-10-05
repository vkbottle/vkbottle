from .base import BaseModel
from .additional import City, Country, Place
from .attachments import MarketPriceCurrency
from enum import IntEnum

import typing

# https://vk.com/dev/objects/group


class CommunityBanInfo(BaseModel):
    end_date: int = None
    comment: str = None


class CommunityContacts(BaseModel):
    user_id: int = None
    desc: str = None
    phone: str = None
    email: str = None


class CommunityCounters(BaseModel):
    photos: int = None
    albums: int = None
    audios: int = None
    videos: int = None
    topics: int = None
    docs: int = None


class CommunityCoverImage(BaseModel):
    url: str = None
    width: int = None
    height: int = None


class CommunityCover(BaseModel):
    enabled: int = None
    images: typing.List[CommunityCoverImage] = None


class CommunityLink(BaseModel):
    id: int = None
    url: str = None
    name: str = None
    desc: str = None
    photo_50: str = None
    photo_100: str = None


class CommunityMainSection(IntEnum):
    no_main_section = 0
    photos = 1
    topics = 2
    audios = 3
    videos = 4
    market = 5


class CommunityMarket(BaseModel):
    enabled: int = None
    price_min: int = None
    price_max: int = None
    main_album_id: int = None
    contact_id: int = None
    currency: MarketPriceCurrency = None
    currency_text: str = None


class CommunityMemberStatus(IntEnum):
    not_a_member = 0
    member = 1
    not_sure = 2
    declined_an_invitation = 3
    sent_request = 4
    invited = 5


class Community(BaseModel):
    id: int = None
    name: str = None
    screen_name: str = None
    is_closed: int = None
    deactivated: str = None
    is_admin: int = None
    admin_level: int = None
    is_member: int = None
    invited_by: int = None
    type: str = None
    has_photo: int = None
    photo_50: str = None
    photo_100: str = None
    photo_200: str = None
    activity: str = None
    age_limits: int = None
    ban_info: CommunityBanInfo = None
    can_create_topic: int = None
    can_message: int = None
    can_post: int = None
    can_see_all_posts: int = None
    can_upload_doc: int = None
    can_upload_video: int = None
    city: City = None
    contacts: CommunityContacts = None
    counters: CommunityCounters = None
    country: Country = None
    cover: CommunityCover = None
    description: str = None
    fixed_post: int = None
    is_favorite: int = None
    is_hidden_from_feed: int = None
    is_messages_blocked: int = None
    links: typing.List[CommunityLink] = None
    main_album_id: int = None
    main_section: CommunityMainSection = None
    market: CommunityMarket = None
    member_status: CommunityMemberStatus = None
    members_count: int = None
    place: Place = None
    public_date_label: str = None
    site: str = None
    start_date: int = None
    finish_date: int = None
    status: str = None
    trending: int = None
    verified: int = None
    wiki_page: str = None
