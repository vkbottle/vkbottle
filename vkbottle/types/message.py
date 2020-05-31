import typing
from datetime import datetime

from vkbottle.api import Api
from vkbottle.framework.framework.extensions import FromExtension
from .client_info import ClientInfo
from .objects.messages import Message as MessageType


def sep_bytes(text: str, max_bytes: int = 4096) -> list:
    text = text.encode("utf-8")
    separation = [text[i : i + max_bytes] for i in range(0, len(text), max_bytes)]
    return list(map(bytes.decode, separation)) if len(separation) else [""]


class GetApi:
    @property
    def api(self) -> Api:
        return Api.get_current()


class Message(MessageType, GetApi):
    client_info: ClientInfo = None

    @property
    def chat_id(self) -> int:
        return self.peer_id - 2000000000

    @property
    def from_chat(self) -> bool:
        return self.peer_id > 2e9

    @property
    def from_user(self) -> bool:
        return self.from_id > 0

    async def reply(
        self,
        message: str = None,
        attachment: str = None,
        user_id: int = None,
        domain: str = None,
        chat_id: int = None,
        random_id: int = FromExtension("random_id"),
        user_ids: typing.List[int] = None,
        lat: typing.Any = None,
        long: typing.Any = None,
        forward_messages: typing.List[int] = None,
        forward: str = None,
        sticker_id: int = None,
        group_id: int = None,
        keyboard: str = None,
        payload: str = None,
        dont_parse_links: bool = None,
        disable_mentions: bool = None,
        template: dict = None,
        intent: str = None,
    ):
        return await self.__call__(
            **self.get_params(locals()), reply_to=self.get_message_id()
        )

    async def __call__(
        self,
        message: str = None,
        attachment: str = None,
        user_id: int = None,
        domain: str = None,
        chat_id: int = None,
        random_id: int = FromExtension("random_id"),
        user_ids: typing.List[int] = None,
        lat: typing.Any = None,
        long: typing.Any = None,
        reply_to: int = None,
        forward_messages: typing.List[int] = None,
        forward: str = None,
        sticker_id: int = None,
        group_id: int = None,
        keyboard: str = None,
        payload: str = None,
        dont_parse_links: bool = None,
        disable_mentions: bool = None,
        template: dict = None,
        intent: str = None,
    ):
        if not message:
            return await self.api.messages.send(
                **self.get_params(locals()), peer_id=self.peer_id,
            )
        _m = []
        for message in sep_bytes(str(message if message is not None else "")):
            _mid = await self.api.messages.send(
                **self.get_params(locals()), peer_id=self.peer_id,
            )
            _m.append(_mid)
        return _m if len(_m) > 1 else _m[0]

    @property
    def date_time(self) -> datetime:
        return datetime.fromtimestamp(self.date)


Message.update_forward_refs()
