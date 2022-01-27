import inspect
import re
import types
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Optional,
    Pattern,
    Tuple,
    Type,
    Union,
)

import vbml

from vkbottle.dispatch.dispenser import get_state_repr
from vkbottle.tools.dev.mini_types.base import BaseMessageMin
from vkbottle.tools.validator import (
    ABCValidator,
    CallableValidator,
    EqualsValidator,
    IsInstanceValidator,
)

if TYPE_CHECKING:
    from vkbottle.dispatch.dispenser.base import BaseStateGroup

from .abc import ABCRule

__all__ = (
    "PeerRule",
    "MentionRule",
    "CommandRule",
    "VBMLRule",
    "StickerRule",
    "FromPeerRule",
    "AttachmentTypeRule",
    "LevenshteinRule",
    "MessageLengthRule",
    "ChatActionRule",
    "PayloadRule",
    "PayloadContainsRule",
    "PayloadMapRule",
    "FromUserRule",
    "FuncRule",
    "CoroutineRule",
    "StateRule",
    "StateGroupRule",
    "RegexRule",
    "MacroRule",
)


DEFAULT_PREFIXES = ["!", "/"]
PayloadMap = List[Tuple[str, Union[type, Callable[[Any], bool], ABCValidator, Any]]]
PayloadMapStrict = List[Tuple[str, ABCValidator]]
PayloadMapDict = Dict[str, Union[dict, type]]


class PeerRule(ABCRule[BaseMessageMin]):
    def __init__(self, from_chat: bool = True):
        self.from_chat = from_chat

    async def check(self, event: BaseMessageMin) -> bool:
        return self.from_chat is (event.peer_id != event.from_id)


class MentionRule(ABCRule[BaseMessageMin]):
    def __init__(self, mention_only: bool = True):
        self.mention_only = mention_only

    async def check(self, event: BaseMessageMin) -> bool:
        if self.mention_only:
            return event.is_mentioned and not event.text
        else:
            return event.is_mentioned


class CommandRule(ABCRule[BaseMessageMin]):
    def __init__(
        self,
        command_text: Union[str, Tuple[str, int]],
        prefixes: Optional[List[str]] = None,
        args_count: int = 0,
        sep: str = " ",
    ):
        self.prefixes = prefixes or DEFAULT_PREFIXES
        self.command_text = command_text if isinstance(command_text, str) else command_text[0]
        self.args_count = args_count if isinstance(command_text, str) else command_text[1]
        self.sep = sep

    async def check(self, event: BaseMessageMin) -> Union[dict, bool]:
        for prefix in self.prefixes:
            if self.args_count == 0 and event.text == prefix + self.command_text:
                return True
            if self.args_count > 0 and event.text.startswith(prefix + self.command_text + " "):
                args = event.text[len(prefix + self.command_text) + 1 :].split(self.sep)
                if len(args) != self.args_count:
                    return False
                elif any(len(arg) == 0 for arg in args):
                    return False
                return {"args": tuple(args)}
        return False


class VBMLRule(ABCRule[BaseMessageMin]):
    def __init__(
        self,
        pattern: Union[str, "vbml.Pattern", Iterable[Union[str, "vbml.Pattern"]]],
        patcher: Optional["vbml.Patcher"] = None,
        flags: Optional[re.RegexFlag] = None,
    ):
        flags = flags or self.config.get("vbml_flags") or re.DOTALL

        if isinstance(pattern, str):
            pattern = [vbml.Pattern(pattern, flags=flags or self.config.get("vbml_flags"))]
        elif isinstance(pattern, vbml.Pattern):
            pattern = [pattern]
        elif isinstance(pattern, Iterable):
            pattern = [
                p if isinstance(p, vbml.Pattern) else vbml.Pattern(p, flags=flags) for p in pattern
            ]

        self.patterns = pattern
        self.patcher = patcher or self.config.get("vbml_patcher") or vbml.Patcher()

    async def check(self, event: BaseMessageMin) -> Union[Optional[dict], bool]:
        for pattern in self.patterns:
            result = self.patcher.check(pattern, event.text)
            if result not in (None, False):
                return result
        return False


class RegexRule(ABCRule[BaseMessageMin]):
    def __init__(self, regexp: Union[str, List[str], Pattern, List[Pattern]]):
        if isinstance(regexp, Pattern):
            regexp = [regexp]
        elif isinstance(regexp, str):
            regexp = [re.compile(regexp)]
        elif isinstance(regexp, list):
            regexp = [re.compile(exp) for exp in regexp]

        self.regexp = regexp

    async def check(self, event: BaseMessageMin) -> Union[dict, bool]:
        for regexp in self.regexp:
            match = re.match(regexp, event.text)
            if match:
                return {"match": match.groups()}
        return False


class StickerRule(ABCRule[BaseMessageMin]):
    def __init__(self, sticker_ids: Union[List[int], int] = None):
        sticker_ids = sticker_ids or []
        if isinstance(sticker_ids, int):
            sticker_ids = [sticker_ids]
        self.sticker_ids = sticker_ids

    async def check(self, event: BaseMessageMin) -> bool:
        if not event.attachments:
            return False
        elif not event.attachments[0].sticker:
            return False
        else:
            if not self.sticker_ids:
                if event.attachments[0].sticker.sticker_id:
                    return True
            elif event.attachments[0].sticker.sticker_id in self.sticker_ids:
                return True
        return False


class FromPeerRule(ABCRule[BaseMessageMin]):
    def __init__(self, peer_ids: Union[List[int], int]):
        if isinstance(peer_ids, int):
            peer_ids = [peer_ids]
        self.peer_ids = peer_ids

    async def check(self, event: BaseMessageMin) -> bool:
        return event.peer_id in self.peer_ids


class AttachmentTypeRule(ABCRule[BaseMessageMin]):
    def __init__(self, attachment_types: Union[List[str], str]):
        if not isinstance(attachment_types, list):
            attachment_types = [attachment_types]
        self.attachment_types = attachment_types

    async def check(self, event: BaseMessageMin) -> bool:
        if not event.attachments:
            return False
        return all(
            attachment.type.value in self.attachment_types for attachment in event.attachments
        )


class ForwardMessagesRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return bool(event.fwd_messages)


class ReplyMessageRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return bool(event.reply_message)


class GeoRule(ABCRule[BaseMessageMin]):
    async def check(self, event: BaseMessageMin) -> bool:
        return bool(event.geo)


class LevenshteinRule(ABCRule[BaseMessageMin]):
    def __init__(self, levenshtein_texts: Union[List[str], str], max_distance: int = 1):
        if isinstance(levenshtein_texts, str):
            levenshtein_texts = [levenshtein_texts]
        self.levenshtein_texts = levenshtein_texts
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

    async def check(self, event: BaseMessageMin) -> bool:
        return any(
            self.distance(event.text, levenshtein_text) <= self.max_distance
            for levenshtein_text in self.levenshtein_texts
        )


class MessageLengthRule(ABCRule[BaseMessageMin]):
    def __init__(self, min_length: int):
        self.min_length = min_length

    async def check(self, event: BaseMessageMin) -> bool:
        return len(event.text) >= self.min_length


class ChatActionRule(ABCRule[BaseMessageMin]):
    def __init__(self, chat_action_types: Union[List[str], str]):
        if isinstance(chat_action_types, str):
            chat_action_types = [chat_action_types]
        self.chat_action_types = chat_action_types

    async def check(self, event: BaseMessageMin) -> bool:
        if not event.action:
            return False
        elif event.action.type.value in self.chat_action_types:
            return True
        return False


class PayloadRule(ABCRule[BaseMessageMin]):
    def __init__(self, payload: Union[dict, List[dict]]):
        if isinstance(payload, dict):
            payload = [payload]
        self.payload = payload

    async def check(self, event: BaseMessageMin) -> bool:
        return event.get_payload_json() in self.payload


class PayloadContainsRule(ABCRule[BaseMessageMin]):
    def __init__(self, payload_particular_part: dict):
        self.payload_particular_part = payload_particular_part

    async def check(self, event: BaseMessageMin) -> bool:
        if event.payload is None:
            return False
        payload = event.get_payload_json()
        if not isinstance(payload, dict):
            return False
        return all(payload.get(k) == v for k, v in self.payload_particular_part.items())


class PayloadMapRule(ABCRule[BaseMessageMin]):
    def __init__(self, payload_map: Union[PayloadMap, PayloadMapDict]):
        if isinstance(payload_map, dict):
            payload_map = self.transform_to_map(payload_map)
        self.payload_map = self.transform_to_callbacks(payload_map)

    @classmethod
    def transform_to_map(cls, payload_map_dict: PayloadMapDict) -> PayloadMap:
        """Transforms PayloadMapDict to PayloadMap"""
        payload_map = []
        for (k, v) in payload_map_dict.items():
            if isinstance(v, dict):
                v = cls.transform_to_map(v)  # type: ignore
            payload_map.append((k, v))
        return payload_map  # type: ignore

    @classmethod
    def transform_to_callbacks(cls, payload_map: PayloadMap) -> PayloadMapStrict:
        """Transforms PayloadMap to PayloadMapStrict"""
        for i, (key, value) in enumerate(payload_map):
            if isinstance(value, type):
                value = IsInstanceValidator(value)
            elif isinstance(value, list):
                value = cls.transform_to_callbacks(value)
            elif isinstance(value, types.FunctionType):
                value = CallableValidator(value)
            elif not isinstance(value, ABCValidator):
                value = EqualsValidator(value)
            payload_map[i] = (key, value)
        return payload_map  # type: ignore

    @classmethod
    async def match(cls, payload: dict, payload_map: PayloadMapStrict):
        """Matches payload with payload_map recursively"""
        for (k, validator) in payload_map:
            if k not in payload:
                return False
            elif isinstance(validator, list):
                if not isinstance(payload[k], dict):
                    return False
                elif not await cls.match(payload[k], validator):
                    return False
            elif not await validator.check(payload[k]):
                return False
        return True

    async def check(self, event: BaseMessageMin) -> bool:
        payload = event.get_payload_json()
        if not isinstance(payload, dict):
            return False
        return await self.match(payload, self.payload_map)


class FromUserRule(ABCRule[BaseMessageMin]):
    def __init__(self, from_user: bool = True):
        self.from_user = from_user

    async def check(self, event: BaseMessageMin) -> bool:
        return self.from_user is (event.from_id > 0)


class FuncRule(ABCRule[BaseMessageMin]):
    def __init__(self, func: Callable[[BaseMessageMin], Union[bool, Awaitable]]):
        self.func = func

    async def check(self, event: BaseMessageMin) -> Union[dict, bool]:
        if inspect.iscoroutinefunction(self.func):
            return await self.func(event)  # type: ignore
        return self.func(event)  # type: ignore


class CoroutineRule(ABCRule[BaseMessageMin]):
    def __init__(self, coroutine: Coroutine):
        self.coro = coroutine

    async def check(self, event: BaseMessageMin) -> Union[dict, bool]:
        return await self.coro


class StateRule(ABCRule[BaseMessageMin]):
    def __init__(
        self,
        state: Optional[Union[List["BaseStateGroup"], "BaseStateGroup"]] = None,
    ):
        if not isinstance(state, list):
            state = [] if state is None else [state]
        self.state = [get_state_repr(s) for s in state]

    async def check(self, event: BaseMessageMin) -> bool:
        if event.state_peer is None:
            return not self.state
        return event.state_peer.state in self.state


class StateGroupRule(ABCRule[BaseMessageMin]):
    def __init__(
        self,
        state_group: Optional[Union[List[Type["BaseStateGroup"]], Type["BaseStateGroup"]]] = None,
    ):
        if not isinstance(state_group, list):
            state_group = [] if state_group is None else [state_group]
        self.state_group = [group.__name__ for group in state_group]

    async def check(self, event: BaseMessageMin) -> bool:
        if event.state_peer is None:
            return not self.state_group
        group_name = event.state_peer.state.split(":", maxsplit=1)[0]
        return group_name in self.state_group


try:
    import macro  # type: ignore
except ImportError:
    macro = None


class MacroRule(ABCRule[BaseMessageMin]):
    def __init__(self, pattern: Union[str, List[str]]):
        if macro is None:
            raise RuntimeError("macro must be installed to use MacroRule")

        if isinstance(pattern, str):
            pattern = [pattern]
        self.patterns = list(map(macro.Pattern, pattern))

    async def check(self, event: BaseMessageMin) -> Union[dict, bool]:
        for pattern in self.patterns:
            result = pattern.check(event.text)
            if result is not None:
                return result
        return False
