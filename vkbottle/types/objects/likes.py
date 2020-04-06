import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class Type(Enum):
    post = "post"
    comment = "comment"
    photo = "photo"
    audio = "audio"
    video = "video"
    note = "note"
    market = "market"
    photo_comment = "photo_comment"
    video_comment = "video_comment"
    topic_comment = "topic_comment"
    market_comment = "market_comment"
    sitepage = "sitepage"
