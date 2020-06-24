from . import photos, base, friends, audio, account
import typing
from enum import Enum
from ..base import BaseModel


class Career(BaseModel):
    city_id: int = None
    company: str = None
    country_id: int = None
    _from: int = None
    group_id: int = None
    id: int = None
    position: str = None
    until: int = None


class CropPhoto(BaseModel):
    crop: "CropPhotoCrop" = None
    photo: "photos.Photo" = None
    rect: "CropPhotoRect" = None


class CropPhotoCrop(BaseModel):
    x: float = None
    x2: float = None
    y: float = None
    y2: float = None


class CropPhotoRect(BaseModel):
    x: float = None
    x2: float = None
    y: float = None
    y2: float = None


class Exports(BaseModel):
    facebook: int = None
    livejournal: int = None
    twitter: int = None


class Fields(Enum):
    photo_id = "photo_id"
    verified = "verified"
    sex = "sex"
    bdate = "bdate"
    city = "city"
    country = "country"
    home_town = "home_town"
    has_photo = "has_photo"
    photo_50 = "photo_50"
    photo_100 = "photo_100"
    photo_200_orig = "photo_200_orig"
    photo_200 = "photo_200"
    photo_400_orig = "photo_400_orig"
    photo_max = "photo_max"
    photo_max_orig = "photo_max_orig"
    online = "online"
    lists = "lists"
    domain = "domain"
    has_mobile = "has_mobile"
    contacts = "contacts"
    site = "site"
    education = "education"
    universities = "universities"
    schools = "schools"
    status = "status"
    last_seen = "last_seen"
    followers_count = "followers_count"
    counters = "counters"
    common_count = "common_count"
    occupation = "occupation"
    nickname = "nickname"
    relatives = "relatives"
    relation = "relation"
    personal = "personal"
    connections = "connections"
    exports = "exports"
    wall_comments = "wall_comments"
    activities = "activities"
    interests = "interests"
    music = "music"
    movies = "movies"
    tv = "tv"
    books = "books"
    games = "games"
    about = "about"
    quotes = "quotes"
    can_post = "can_post"
    can_see_all_posts = "can_see_all_posts"
    can_see_audio = "can_see_audio"
    can_write_private_message = "can_write_private_message"
    can_send_friend_request = "can_send_friend_request"
    is_favorite = "is_favorite"
    is_hidden_from_feed = "is_hidden_from_feed"
    timezone = "timezone"
    screen_name = "screen_name"
    maiden_name = "maiden_name"
    crop_photo = "crop_photo"
    is_friend = "is_friend"
    friend_status = "friend_status"
    career = "career"
    military = "military"
    blacklisted = "blacklisted"
    blacklisted_by_me = "blacklisted_by_me"
    can_subscribe_posts = "can_subscribe_posts"
    descriptions = "descriptions"
    trending = "trending"
    mutual = "mutual"


class LastSeen(BaseModel):
    platform: int = None
    time: int = None


class Military(BaseModel):
    country_id: int = None
    _from: int = None
    id: int = None
    unit: str = None
    unit_id: int = None
    until: int = None


class Occupation(BaseModel):
    id: int = None
    name: str = None
    type: str = None


class Personal(BaseModel):
    alcohol: int = None
    inspired_by: str = None
    langs: typing.List = None
    life_main: int = None
    people_main: int = None
    political: int = None
    religion: str = None
    religion_id: int = None
    smoking: int = None


class Relative(BaseModel):
    birth_date: str = None
    id: int = None
    name: str = None
    type: str = None


class School(BaseModel):
    city: int = None
    _class: str = None
    country: int = None
    id: str = None
    name: str = None
    type: int = None
    type_str: str = None
    year_from: int = None
    year_graduated: int = None
    year_to: int = None


class University(BaseModel):
    chair: int = None
    chair_name: str = None
    city: int = None
    country: int = None
    education_form: str = None
    education_status: str = None
    faculty: int = None
    faculty_name: str = None
    graduation: int = None
    id: int = None
    name: str = None


class UserConnections(BaseModel):
    skype: str = None
    facebook: str = None
    facebook_name: str = None
    twitter: str = None
    livejournal: str = None
    instagram: str = None


class UserCounters(BaseModel):
    albums: int = None
    audios: int = None
    followers: int = None
    friends: int = None
    gifts: int = None
    groups: int = None
    notes: int = None
    online_friends: int = None
    pages: int = None
    photos: int = None
    subscriptions: int = None
    user_photos: int = None
    user_videos: int = None
    videos: int = None


class UserMin(BaseModel):
    deactivated: str = None
    first_name: str = None
    hidden: int = None
    id: int = None
    last_name: str = None
    can_access_closed: bool = None
    is_closed: bool = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class User(UserMin):
    sex: "base.Sex" = None
    screen_name: str = None
    photo_50: str = None
    photo_100: str = None
    online: "base.BoolInt" = None
    online_mobile: "base.BoolInt" = None
    online_app: int = None
    verified: "base.BoolInt" = None
    trending: "base.BoolInt" = None
    friend_status: int = None
    mutual: "friends.RequestsMutual" = None


class UserFull(User):
    nickname: str = None
    maiden_name: str = None
    domain: str = None
    bdate: str = None
    city: "base.Object" = None
    country: "base.Country" = None
    timezone: int = None
    photo_200: str = None
    photo_max: str = None
    photo_200_orig: str = None
    photo_400_orig: str = None
    photo_max_orig: str = None
    photo_id: str = None
    has_photo: "base.BoolInt" = None
    has_mobile: "base.BoolInt" = None
    is_friend: "base.BoolInt" = None
    wall_comments: "base.BoolInt" = None
    can_post: "base.BoolInt" = None
    can_see_all_posts: "base.BoolInt" = None
    can_see_audio: "base.BoolInt" = None
    can_write_private_message: "base.BoolInt" = None
    can_send_friend_request: "base.BoolInt" = None
    mobile_phone: str = None
    home_phone: str = None
    site: str = None
    status_audio: "audio.Audio" = None
    status: str = None
    activity: str = None
    last_seen: "LastSeen" = None
    exports: "Exports" = None
    crop_photo: "CropPhoto" = None
    followers_count: int = None
    blacklisted: "base.BoolInt" = None
    blacklisted_by_me: "base.BoolInt" = None
    is_favorite: "base.BoolInt" = None
    is_hidden_from_feed: "base.BoolInt" = None
    common_count: int = None
    occupation: "Occupation" = None
    career: typing.List = None
    military: typing.List = None
    university: int = None
    university_name: str = None
    faculty: int = None
    faculty_name: str = None
    graduation: int = None
    education_form: str = None
    education_status: str = None
    home_town: str = None
    relation: int = None
    relation_partner: "UserMin" = None
    personal: "Personal" = None
    universities: typing.List = None
    schools: typing.List = None
    relatives: typing.List = None
    is_subscribed_podcasts: bool = None
    can_subscribe_podcasts: bool = None
    can_subscribe_posts: bool = None


class UserSettingsXtr(BaseModel):
    connections: "UserConnections" = None
    bdate: str = None
    bdate_visibility: int = None
    city: "base.City" = None
    country: "base.Country" = None
    first_name: str = None
    home_town: str = None
    last_name: str = None
    maiden_name: str = None
    name_request: "account.NameRequest" = None
    personal: "Personal" = None
    phone: str = None
    relation: int = None
    relation_partner: "UserMin" = None
    relation_pending: "base.BoolInt" = None
    relation_requests: typing.List = None
    screen_name: str = None
    sex: "base.Sex" = None
    status: str = None
    status_audio: "audio.Audio" = None
    interests: "account.UserSettingsInterests" = None
    languages: typing.List = None


class UserType(Enum):
    profile = "profile"


class UserXtrCounters(UserFull):
    counters: "UserCounters" = None


class UserXtrType(User):
    type: "UserType" = None


class UsersArray(BaseModel):
    count: int = None
    items: typing.List = None


class UserXtrLists(UserFull):
    lists: typing.List = None


class UserXtrPhone(UserFull):
    phone: str = None


class UserSettings(UserMin, UserSettingsXtr):
    pass


Career.update_forward_refs()
CropPhoto.update_forward_refs()
CropPhotoCrop.update_forward_refs()
CropPhotoRect.update_forward_refs()
Exports.update_forward_refs()
LastSeen.update_forward_refs()
Military.update_forward_refs()
Occupation.update_forward_refs()
Personal.update_forward_refs()
Relative.update_forward_refs()
School.update_forward_refs()
University.update_forward_refs()
User.update_forward_refs()
UserConnections.update_forward_refs()
UserCounters.update_forward_refs()
UserFull.update_forward_refs()
UserMin.update_forward_refs()
UserSettings.update_forward_refs()
UserSettingsXtr.update_forward_refs()
UserXtrCounters.update_forward_refs()
UserXtrLists.update_forward_refs()
UserXtrPhone.update_forward_refs()
UserXtrType.update_forward_refs()
UsersArray.update_forward_refs()
