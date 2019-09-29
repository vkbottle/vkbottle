from .base import BaseModel

from .additional import City, Country
from .attachments import CropPhoto
from enum import IntEnum

import typing

# https://vk.com/dev/objects/user


class UserCareer(BaseModel):
    group_id: int = None
    company: str = None
    country_id: int = None
    city_id: int = None
    city_name: str = None
    from_: int = None
    until: int = None
    position: str = None


class UserCounters(BaseModel):
    albums: int = None
    videos: int = None
    audios: int = None
    photo: int = None
    notes: int = None
    friends: int = None
    groups: int = None
    online_friends: int = None
    mutual_friends: int = None
    user_videos: int = None
    followers: int = None
    pages: int = None


class UserContacts(BaseModel):
    mobile_phone: str = None
    home_phone: str = None


class UserEducation(BaseModel):
    university: int = None
    university_name: str = None
    faculty: int = None
    faculty_name: str = None
    graduation: int = None


class UserPlatform(IntEnum):
    m_vk_com = 1
    iphone = 2
    ipad = 3
    android = 4
    windows_phone_app = 5
    windows_8_app = 6
    web = 7
    vk_com = 7
    vk_mobile = 8


class UserLastSeen(BaseModel):
    time: int = None
    platform: UserPlatform = None


class UserMilitary(BaseModel):
    unit: str = None
    unit_id: int = None
    country_id: int = None
    from_: int = None
    until: int = None


class UserOccupation(BaseModel):
    type: str = None
    id: int = None
    name: str = None


class Political(IntEnum):
    communist = 1
    socialist = 2
    moderate = 3
    liberal = 4
    conservative = 5
    monarchist = 6
    ultraconservative = 7
    apathetic = 8
    libertarian = 9


class PeopleMain(IntEnum):
    intelect = 1
    creativity = 1
    kindness = 2
    honesty = 2
    health = 3
    beauty = 3
    wealth = 4
    power = 4
    courage = 5
    persistance = 5
    humor = 6
    love_for_life = 6


class LifeMain(IntEnum):
    family = 1
    children = 1
    career = 2
    money = 2
    entertainment = 3
    leisure = 3
    science = 4
    research = 4
    improving_the_world = 5
    personal_development = 6
    beaty = 7
    art = 7
    fame = 8
    influence = 8


class Smoking(IntEnum):
    very_negative = 1
    negative = 2
    neutral = 3
    compromisable = 4
    positive = 5


class Alcohol(BaseModel):
    very_negative = 1
    negative = 2
    neutral = 3
    compromisable = 4
    positive = 5


class UserPersonal(BaseModel):
    political: Political = None
    langs: typing.List[str] = None
    religion: str = None
    inspired_by: str = None
    people_main: PeopleMain = None
    life_main: LifeMain = None
    smoking: Smoking = None
    alcohol: Alcohol = None


class UserRelation(IntEnum):
    single = 1
    in_relationship = 2
    engaged = 3
    married = 4
    complicated = 5
    actively_searching = 6
    in_love = 7
    in_civil_union = 8
    not_specified = 0


class SchoolType(IntEnum):
    school = 0
    gymnasium = 1
    lyceum = 2
    boarding_school = 3
    evening_school = 4
    music_school = 5
    sport_school = 6
    artistic_school = 7
    college = 8
    professional_lyceum = 9
    technical_college = 10
    vocational = 11
    specialized_school = 12
    art_school = 13


class School(BaseModel):
    id: int = None
    country: int = None
    city: int = None
    name: str = None
    year_from: int = None
    year_to: int = None
    year_graduated: int = None
    class_: str = None
    speciality: str = None
    type: int = None
    type_str: SchoolType = None


class Universitiy(BaseModel):
    id: int = None
    country: int = None
    city: int = None
    name: str = None
    faculty: int = None
    faculty_name: str = None
    chair: int = None
    chair_name: str = None
    graduation: int = None
    education_form: str = None
    education_status: str = None


class User(BaseModel):
    id: int = None
    first_name: str = None
    last_name: str = None
    deactivated: str = None
    is_closed: bool = None
    can_access_closed: bool = None
    about: str = None
    activities: str = None
    bdate: str = None
    blacklisted: int = None
    blacklisted_by_me: int = None
    books: str = None
    can_post: int = None
    can_see_all_posts: int = None
    can_see_audio: int = None
    can_send_friend_request: int = None
    can_write_private_message: int = None
    career: UserCareer = None
    city: City = None
    common_count: int = None
    contacts: UserContacts = None
    counters: UserCounters = None
    country: Country = None
    crop_photo: CropPhoto = None
    domain: str = None
    education: UserEducation = None
    followers_count: int = None
    friend_status: int = None
    games: str = None
    has_mobile: int = None
    has_photo: int = None
    home_town: str = None
    interests: str = None
    is_favorite: int = None
    is_friend: int = None
    is_hidden_from_feed: int = None
    last_seen: UserLastSeen = None
    lists: typing.List[int] = None
    maiden_name: str = None
    military: UserMilitary = None
    movies: str = None
    music: str = None
    nickname: str = None
    occupation: UserOccupation = None
    online: int = None
    personal: UserPersonal = None
    photo_50: str = None
    photo_100: str = None
    photo_200_orig: str = None
    photo_200: str = None
    photo_400_orig: str = None
    photo_id: str = None
    photo_max: str = None
    photo_max_orig: str = None
    quotes: str = None
    relatives: typing.List = None
    relation: UserRelation = None
    schools: typing.List[School] = None
    screen_name: str = None
    sex: int = None
    site: str = None
    status: str = None
    timezone: int = None
    trending: int = None
    tv: str = None
    universities: typing.List[Universitiy] = None
    verified: int = None
    wall_comments: int = None
