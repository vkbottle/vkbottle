from . import audio
from ..base import BaseModel


class Status(BaseModel):
    audio: "audio.Audio" = None
    text: str = None


Status.update_forward_refs()
