from abc import ABC, abstractmethod
from typing import Callable, Any, Dict, Type, List, Union

from vbml import Patcher

from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.views import ABCView
from vkbottle.dispatch.rules.bot import (
    PeerRule,
    VBMLRule,
    CommandRule,
    FromUserRule,
    FromPeerRule,
    StickerRule,
    AttachmentTypeRule,
    LevensteinRule,
    MessageLengthRule,
    ChatActionRule,
    PayloadRule,
    PayloadContainsRule,
    PayloadMapRule,
    FuncRule,
    CoroutineRule,
    StateRule,
)
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin

LabeledMessageHandler = Callable[..., Callable[[MessageMin], Any]]
LabeledHandler = Callable[..., Callable[[Any], Any]]

DEFAULT_CUSTOM_RULES: Dict[str, Type[ABCRule]] = {
    "from_chat": PeerRule,
    "command": CommandRule,
    "from_user": FromUserRule,
    "peer_ids": FromPeerRule,
    "sticker": StickerRule,
    "attachment": AttachmentTypeRule,
    "levenstein": LevensteinRule,
    "lev": LevensteinRule,
    "length": MessageLengthRule,
    "action": ChatActionRule,
    "payload": PayloadRule,
    "payload_contains": PayloadContainsRule,
    "payload_map": PayloadMapRule,
    "func": FuncRule,
    "coro": CoroutineRule,
    "coroutine": CoroutineRule,
    "state": StateRule,
}


class ABCBotLabeler(ABC):
    def __init_subclass__(cls, **kwargs):
        cls.patcher = kwargs.get("patcher") or Patcher()
        cls.custom_rules = kwargs.get("custom_rules") or DEFAULT_CUSTOM_RULES
        cls.custom_rules["text"] = cls.get_vbml_rule  # type: ignore

    @abstractmethod
    def message(self, *rules: "ABCRule", **custom_rules) -> LabeledMessageHandler:
        pass

    @abstractmethod
    def chat_message(self, *rules: "ABCRule", **custom_rules) -> LabeledMessageHandler:
        pass

    @abstractmethod
    def private_message(self, *rules: "ABCRule", **custom_rules) -> LabeledMessageHandler:
        pass

    @abstractmethod
    def raw_event(
        self,
        event: Union[str, List[str]],
        dataclass: Callable = dict,
        *rules: "ABCRule",
        **custom_rules,
    ) -> LabeledHandler:
        pass

    @abstractmethod
    def views(self) -> Dict[str, "ABCView"]:
        pass

    @abstractmethod
    def load(self, labeler: Any):
        pass

    def get_custom_rules(self, custom_rules: Dict[str, Any]) -> List["ABCRule"]:
        return [self.custom_rules[k](v) for k, v in custom_rules.items()]  # type: ignore

    @classmethod
    def get_vbml_rule(cls, pattern: Any) -> "VBMLRule":
        return VBMLRule(pattern, getattr(cls, "patcher"))
