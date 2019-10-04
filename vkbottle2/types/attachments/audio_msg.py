from ..base import BaseModel
from typing import List


class AudioMsg(BaseModel):
    duration: int = None
    waveform: List[int] = None
    link_ogg: str = None
    link_mp3: str = None
