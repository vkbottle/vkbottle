from . import audio
import typing
from enum import Enum
from ..base import BaseModel
from vkbottle.types import objects


class Status(BaseModel):
    audio: "audio.Audio" = None
    text: str = None


Status.update_forward_refs()
