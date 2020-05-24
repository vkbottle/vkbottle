from vkbottle.types.base import BaseModel
from vkbottle.types.message import sep_bytes
from vkbottle.types.objects.messages import MessageAction
from vkbottle.types.objects.base import Geo
from vkbottle.api import UserApi
import random
import typing


class GetApi:
    @property
    def api(self) -> UserApi:
        return UserApi.get_current()


class Message(BaseModel, GetApi):
    message_id: int = None
    flags: int = None
    peer_id: int = None
    timestamp: int = None
    text: str = None
    attachments: typing.Union[list, dict] = None
    random_id: int = None
    # from messages.getById
    id: int = None
    conversation_message_id: int = None
    from_id: int = None
    date: int = None
    out: int = None
    read_state: int = None
    ref: str = None
    ref_source: str = None
    important: bool = None
    geo: Geo = None
    reply_message: "Message" = None
    fwd_messages: typing.List["Message"] = None
    action: MessageAction = None

    async def get(self) -> dict:
        return (
            await self.api.request("messages.getById", {"message_ids": self.message_id})
        )["items"][0]

    @property
    def chat_id(self) -> int:
        return self.peer_id - 2000000000

    async def reply(self, message: str = None, attachment: str = None, **params):

        locals().update(params)
        return await self.api.request(
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
        m = None
        locals().update(params)
        for message in sep_bytes(message or ""):
            m = await self.api.request(
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


Message.update_forward_refs()
