from .base import BaseModel
from .attachments import Photo

from enum import Enum, IntEnum

import typing


# https://vk.com/dev/objects/app


class ApplicationType(Enum):
    app = "social app"
    game = "game"
    site = "site"
    standalone = "standalone"


class LeaderBoardType(IntEnum):
    not_supported = 0
    by_level = 1
    by_points = 2


class Application(BaseModel):
    id: int = None
    title: str = None
    icon_278: str = None
    icon_139: str = None
    icon_150: str = None
    icon_75: str = None
    banner_560: str = None
    banner_1120: str = None
    type: ApplicationType = None
    section: str = None
    author_url: str = None
    author_id: int = None
    author_group: int = None
    members_count: int = None
    published_date: int = None
    catalog_position: int = None
    international: int = None
    leaderboard_type: LeaderBoardType = None
    genre_id: int = None
    genre: str = None
    platform_id: str = None
    is_in_catalog: int = None
    description: str = None
    screen_name: str = None
    icon_16: str = None
    screenshots: typing.List[Photo] = None
