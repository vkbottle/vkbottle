import typing
from enum import Enum
from ..base import BaseModel


class AppMin(BaseModel):
    type: "AppType" = None
    id: int = None
    title: str = None
    author_id: int = None
    icon_139: str = None
    icon_150: str = None
    icon_278: str = None
    icon_75: str = None

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id


class App(AppMin):
    author_group: int = None
    author_url: str = None
    banner_1120: str = None
    banner_560: str = None
    friends: typing.List = None
    catalog_position: int = None
    description: str = None
    genre: str = None
    genre_id: int = None
    international: int = None
    is_in_catalog: int = None
    leaderboard_type: int = None
    members_count: int = None
    platform_id: int = None
    published_date: int = None
    screen_name: str = None
    screenshots: typing.List = None
    section: str = None


class AppType(Enum):
    app = "app"
    game = "game"
    site = "site"
    standalone = "standalone"
    vk_app = "vk_app"
    community_app = "community_app"
    html5_game = "html5_game"


class Leaderboard(BaseModel):
    level: int = None
    points: int = None
    score: int = None
    user_id: int = None


class Scope(BaseModel):
    name: str = None
    title: str = None


App.update_forward_refs()
AppMin.update_forward_refs()
Leaderboard.update_forward_refs()
Scope.update_forward_refs()
