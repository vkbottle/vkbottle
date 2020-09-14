from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Type

from vbml import Patcher

from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.rules.bot import AttachmentTypeRule
from vkbottle.dispatch.rules.bot import ChatActionRule
from vkbottle.dispatch.rules.bot import CommandRule
from vkbottle.dispatch.rules.bot import FromPeerRule
from vkbottle.dispatch.rules.bot import FromUserRule
from vkbottle.dispatch.rules.bot import FuncRule
from vkbottle.dispatch.rules.bot import LevensteinRule
from vkbottle.dispatch.rules.bot import MessageLengthRule
from vkbottle.dispatch.rules.bot import PayloadContainsRule
from vkbottle.dispatch.rules.bot import PayloadMapRule
from vkbottle.dispatch.rules.bot import PayloadRule
from vkbottle.dispatch.rules.bot import PeerRule
from vkbottle.dispatch.rules.bot import StickerRule
from vkbottle.dispatch.rules.bot import VBMLRule
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin

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
    "func": FuncRule,
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
