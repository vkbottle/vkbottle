from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Union

from vkbottle_types.events import GroupEventType

from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.views import ABCView
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin

LabeledMessageHandler = Callable[..., Callable[[MessageMin], Any]]
LabeledHandler = Callable[..., Callable[[Any], Any]]
EventName = Union[GroupEventType, str]


class ABCBotLabeler(ABC):
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
        event: Union[EventName, List[EventName]],
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
