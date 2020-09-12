from abc import ABC, abstractmethod
from vkbottle.dispatch.rules import ABCRule
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
)
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from typing import Callable, Any, Dict, Optional, Type, List
from vbml import Patcher

LabeledMessageHandler = Callable[..., Callable[[MessageMin], Any]]

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
}


class ABCBotLabeler(ABC):
    def __init__(
        self,
        custom_rules: Optional[Dict[str, Type["ABCRule"]]] = None,
        patcher: Optional[Patcher] = None,
    ):
        self.patcher = patcher or Patcher()
        self.custom_rules = custom_rules or DEFAULT_CUSTOM_RULES
        self.custom_rules["text"] = self.get_vbml_rule  # type: ignore

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
    def load(self, labeler: Any):
        pass

    def get_custom_rules(self, custom_rules: Dict[str, Any]) -> List["ABCRule"]:
        return [self.custom_rules[k](v) for k, v in custom_rules.items()]  # type: ignore

    def get_vbml_rule(self, pattern: Any) -> "VBMLRule":
        return VBMLRule(pattern, self.patcher)
