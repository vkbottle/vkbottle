from .abc import ABCRule
from abc import abstractmethod
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from typing import List, Optional, Union
import vbml


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
            if result is not None:
                return result
        return False


__all__ = (
    "ABCMessageRule",
    "PeerRule",
    "CommandRule",
    "VBMLRule",
)
