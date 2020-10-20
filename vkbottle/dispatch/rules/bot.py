from .abc import ABCRule
from abc import abstractmethod
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from vkbottle_types import BaseStateGroup
from typing import List, Optional, Union, Tuple, Callable, Awaitable, Coroutine
import vbml
import inspect


DEFAULT_PREFIXES = ["!", "/"]
Message = MessageMin


class ABCMessageRule(ABCRule):
    @abstractmethod
    async def check(self, message: Message) -> bool:
        pass


class PeerRule(ABCMessageRule):
    def __init__(self, from_chat: bool = True):
        self.from_chat = from_chat

    async def check(self, message: Message) -> bool:
        if message.peer_id != message.from_id:
            return self.from_chat
        return not self.from_chat


class CommandRule(ABCMessageRule):
    def __init__(self, command_text: str, prefixes: Optional[List[str]] = None):
        self.prefixes = prefixes or DEFAULT_PREFIXES
        self.command_text = command_text

    async def check(self, message: Message) -> bool:
        for prefix in self.prefixes:
            if message.text == prefix + self.command_text:
                return True
        return False


class VBMLRule(ABCMessageRule):
    def __init__(
        self,
        pattern: Union[str, "vbml.Pattern", List[Union[str, "vbml.Pattern"]]],
        patcher: "vbml.Patcher",
    ):
        if isinstance(pattern, str):
            pattern = [vbml.Pattern(pattern)]
        elif isinstance(pattern, vbml.Pattern):
            pattern = [pattern]
        elif isinstance(pattern, list):
            pattern = [p if isinstance(p, vbml.Pattern) else vbml.Pattern(p) for p in pattern]
        self.patterns = pattern
        self.patcher = patcher

    async def check(self, message: Message) -> bool:
        for pattern in self.patterns:
            result = self.patcher.check(pattern, message.text)
            if result not in (None, False):
                return result
        return False


class StickerRule(ABCMessageRule):
    def __init__(self, sticker_ids: Union[List[int], int]):
        if isinstance(sticker_ids, int):
            sticker_ids = [sticker_ids]
        self.sticker_ids = sticker_ids

    async def check(self, message: Message) -> bool:
        if not message.attachments:
            return False
        elif not message.attachments[0].sticker:
            return False
        elif message.attachments[0].sticker.sticker_id in self.sticker_ids:
            return True
        return False


class FromPeerRule(ABCMessageRule):
    def __init__(self, peer_ids: Union[List[int], int]):
        if isinstance(peer_ids, int):
            peer_ids = [peer_ids]
        self.peer_ids = peer_ids

    async def check(self, message: Message) -> bool:
        if message.peer_id in self.peer_ids:
            return True


class AttachmentTypeRule(ABCMessageRule):
    def __init__(self, attachment_types: Union[List[str], str]):
        if not isinstance(attachment_types, list):
            attachment_types = [attachment_types]
        self.attachment_types = attachment_types

    async def check(self, message: Message) -> bool:
        if not message.attachments:
            return False
        for attachment in message.attachments:
            if attachment.type not in self.attachment_types:
                return False
        return True


class LevensteinRule(ABCMessageRule):
    def __init__(self, levenstein_texts: Union[List[str], str], max_distance: int = 1):
        if isinstance(levenstein_texts, str):
            levenstein_texts = [levenstein_texts]
        self.levenstein_texts = levenstein_texts
        self.max_distance = max_distance

    @staticmethod
    def distance(a: str, b: str) -> int:
        n, m = len(a), len(b)
        if n > m:
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n  # type: ignore
            for j in range(1, n + 1):
                add, delete, change = (
                    previous_row[j] + 1,
                    current_row[j - 1] + 1,
                    previous_row[j - 1],
                )
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)  # type: ignore

        return current_row[n]

    async def check(self, message: Message) -> bool:
        for levenstein_text in self.levenstein_texts:
            if self.distance(message.text, levenstein_text) <= self.max_distance:
                return True
        return False


class MessageLengthRule(ABCMessageRule):
    def __init__(self, min_length: int):
        self.min_length = min_length

    async def check(self, message: Message) -> bool:
        if len(message.text) >= self.min_length:
            return True
        return False


class ChatActionRule(ABCMessageRule):
    def __init__(self, chat_action_types: Union[List[str], str]):
        if isinstance(chat_action_types, str):
            chat_action_types = [chat_action_types]
        self.chat_action_types = chat_action_types

    async def check(self, message: Message) -> bool:
        if not message.action:
            return False
        elif message.action.type in self.chat_action_types:
            return True
        return False


class PayloadRule(ABCMessageRule):
    def __init__(self, payload: dict):
        self.payload = payload

    async def check(self, message: Message) -> bool:
        return message.get_payload_json() == self.payload


class PayloadContainsRule(ABCMessageRule):
    def __init__(self, payload_particular_part: dict):
        self.payload_particular_part = payload_particular_part

    async def check(self, message: Message) -> bool:
        payload = message.get_payload_json(unpack_failure=lambda p: {})
        for k, v in self.payload_particular_part.items():
            if payload.get(k) != v:
                return False
        return True


class PayloadMapRule(ABCMessageRule):
    def __init__(self, payload_map: List[Tuple[str, type]]):
        self.payload_map = payload_map

    async def check(self, message: Message) -> bool:
        payload = message.get_payload_json(unpack_failure=lambda p: {})
        for (k, v_type) in self.payload_map:
            if k not in payload:
                return False
            elif not isinstance(payload[k], v_type):
                return False
        return True


class FromUserRule(ABCMessageRule):
    def __init__(self, from_user: bool = True):
        self.from_user = from_user

    async def check(self, message: Message) -> bool:
        if message.from_id > 0:
            return True
        return False


class FuncRule(ABCMessageRule):
    def __init__(self, func: Union[Callable[[Message], Union[bool, Awaitable]]]):
        self.func = func

    async def check(self, message: Message) -> bool:
        if inspect.iscoroutinefunction(self.func):
            return await self.func(message)  # type: ignore
        return self.func(message)  # type: ignore


class CoroutineRule(ABCMessageRule):
    def __init__(self, coroutine: Coroutine):
        self.coro = coroutine

    async def check(self, message: Message) -> bool:
        return await self.coro


class StateRule(ABCMessageRule):
    def __init__(self, state: Union[List[BaseStateGroup], BaseStateGroup]):
        if not isinstance(state, list):
            state = [state]
        self.state = state

    async def check(self, message: Message) -> bool:
        if message.state_peer is None:
            return False
        return message.state_peer.state in self.state


__all__ = (
    "ABCMessageRule",
    "PeerRule",
    "CommandRule",
    "VBMLRule",
    "StickerRule",
    "FromPeerRule",
    "AttachmentTypeRule",
    "LevensteinRule",
    "MessageLengthRule",
    "ChatActionRule",
    "PayloadRule",
    "PayloadContainsRule",
    "PayloadMapRule",
    "FromUserRule",
    "FuncRule",
    "CoroutineRule",
    "StateRule",
)
