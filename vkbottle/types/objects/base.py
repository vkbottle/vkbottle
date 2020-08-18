import typing
from enum import Enum, IntEnum
from ..base import BaseModel


BoolInt = int


class City(BaseModel):
    id: int = None
    title: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class CommentsInfo(BaseModel):
    can_post: "BoolInt" = None
    count: int = None
    groups_can_post: bool = None


class Country(BaseModel):
    id: int = None
    title: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class Error(BaseModel):
    error_code: int = None
    error_msg: str = None
    request_params: typing.List = None


class Geo(BaseModel):
    coordinates: "GeoCoordinates" = None
    place: "Place" = None
    showmap: int = None
    type: str = None


class GeoCoordinates(BaseModel):
    latitude: float = None
    longitude: float = None


class Image(BaseModel):
    height: int = None
    url: str = None
    width: int = None


class Likes(BaseModel):
    count: int = None
    user_likes: "BoolInt" = None


class LikesInfo(BaseModel):
    can_like: "BoolInt" = None
    can_publish: "BoolInt" = None
    count: int = None
    user_likes: int = None


class MessageError(BaseModel):
    code: int = None
    description: str = None


class Object(BaseModel):
    id: int = None
    title: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class ObjectCount(BaseModel):
    count: int = None


class ObjectWithName(BaseModel):
    id: int = None
    name: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class OkResponse(IntEnum):
    ok = 1


class Place(BaseModel):
    address: str = None
    checkins: int = None
    city: str = None
    country: str = None
    created: int = None
    icon: str = None
    id: int = None
    latitude: float = None
    longitude: float = None
    title: str = None
    type: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class PropertyExists(IntEnum):
    exists = 1


class RepostsInfo(BaseModel):
    count: int = None
    user_reposted: int = None


class RequestParam(BaseModel):
    key: str = None
    value: str = None


class Sex(IntEnum):
    no = 0
    female = 1
    male = 2


class StickerImages(BaseModel):
    url: str = None
    width: int = None
    height: int = None


class Sticker(BaseModel):
    images: typing.List[StickerImages] = None
    images_with_background: typing.List[StickerImages] = None
    product_id: int = None
    sticker_id: int = None

    def __hash__(self):
        return hash((self.product_id, self.sticker_id))

    def __eq__(self, other):
        return (
            self.product_id == other.product_id and self.sticker_id == other.sticker_id
        )


class UploadServer(BaseModel):
    upload_url: str = None


class UserGroupFields(Enum):
    about = "about"
    action_button = "action_button"
    activities = "activities"
    activity = "activity"
    addresses = "addresses"
    admin_level = "admin_level"
    age_limits = "age_limits"
    author_id = "author_id"
    ban_info = "ban_info"
    bdate = "bdate"
    blacklisted = "blacklisted"
    blacklisted_by_me = "blacklisted_by_me"
    books = "books"
    can_create_topic = "can_create_topic"
    can_message = "can_message"
    can_post = "can_post"
    can_see_all_posts = "can_see_all_posts"
    can_see_audio = "can_see_audio"
    can_send_friend_request = "can_send_friend_request"
    can_upload_video = "can_upload_video"
    can_write_private_message = "can_write_private_message"
    career = "career"
    city = "city"
    common_count = "common_count"
    connections = "connections"
    contacts = "contacts"
    counters = "counters"
    country = "country"
    cover = "cover"
    crop_photo = "crop_photo"
    deactivated = "deactivated"
    description = "description"
    domain = "domain"
    education = "education"
    exports = "exports"
    finish_date = "finish_date"
    fixed_post = "fixed_post"
    followers_count = "followers_count"
    friend_status = "friend_status"
    games = "games"
    has_market_app = "has_market_app"
    has_mobile = "has_mobile"
    has_photo = "has_photo"
    home_town = "home_town"
    id = "id"
    interests = "interests"
    is_admin = "is_admin"
    is_closed = "is_closed"
    is_favorite = "is_favorite"
    is_friend = "is_friend"
    is_hidden_from_feed = "is_hidden_from_feed"
    is_member = "is_member"
    is_messages_blocked = "is_messages_blocked"
    can_send_notify = "can_send_notify"
    is_subscribed = "is_subscribed"
    last_seen = "last_seen"
    links = "links"
    lists = "lists"
    maiden_name = "maiden_name"
    main_album_id = "main_album_id"
    main_section = "main_section"
    market = "market"
    member_status = "member_status"
    members_count = "members_count"
    military = "military"
    movies = "movies"
    music = "music"
    name = "name"
    nickname = "nickname"
    occupation = "occupation"
    online = "online"
    online_status = "online_status"
    personal = "personal"
    phone = "phone"
    photo_100 = "photo_100"
    photo_200 = "photo_200"
    photo_200_orig = "photo_200_orig"
    photo_400_orig = "photo_400_orig"
    photo_50 = "photo_50"
    photo_id = "photo_id"
    photo_max = "photo_max"
    photo_max_orig = "photo_max_orig"
    quotes = "quotes"
    relation = "relation"
    relatives = "relatives"
    schools = "schools"
    screen_name = "screen_name"
    sex = "sex"
    site = "site"
    start_date = "start_date"
    status = "status"
    timezone = "timezone"
    trending = "trending"
    tv = "tv"
    type = "type"
    universities = "universities"
    verified = "verified"
    wall_comments = "wall_comments"
    wiki_page = "wiki_page"
    vk_admin_status = "vk_admin_status"


class UserId(BaseModel):
    user_id: int = None


City.update_forward_refs()
CommentsInfo.update_forward_refs()
Country.update_forward_refs()
Error.update_forward_refs()
Geo.update_forward_refs()
GeoCoordinates.update_forward_refs()
Image.update_forward_refs()
Likes.update_forward_refs()
LikesInfo.update_forward_refs()
MessageError.update_forward_refs()
Object.update_forward_refs()
ObjectCount.update_forward_refs()
ObjectWithName.update_forward_refs()
Place.update_forward_refs()
RepostsInfo.update_forward_refs()
RequestParam.update_forward_refs()
StickerImages.update_forward_refs()
Sticker.update_forward_refs()
UploadServer.update_forward_refs()
UserId.update_forward_refs()
