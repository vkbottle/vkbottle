from .base import BaseModel
from .message import sep_bytes
from ..api import UserApi
import random

API = UserApi.get_current


class Message(BaseModel):
    message_id: int = None
    flags: int = None
    peer_id: int = None
    timestamp: int = None
    text: str = None
    attachments: dict = None
    random_id: int = None

    async def reply(self, message: str = None, attachment: str = None, **params):

        locals().update(params)
        return await API().request(
            "messages.send",
            dict(
                peer_id=self.peer_id,
                reply_to=self.message_id,
                random_id=random.randint(-2e9, 2e9),
                **{
                    k: v
                    for k, v in locals().items()
                    if v is not None and k not in ["self", "params"]
                }
            ),
        )

    async def __call__(self, message: str = None, attachment: str = None, **params):

        locals().update(params)
        for message in sep_bytes(message or ""):
            m = await API().request(
                "messages.send",
                dict(
                    peer_id=self.peer_id,
                    random_id=random.randint(-2e9, 2e9),
                    **{
                        k: v
                        for k, v in locals().items()
                        if v is not None and k not in ["self", "params"]
                    }
                ),
            )
        return m
