from abc import ABC, abstractmethod
from vkbottle.dispatch.rules import ABCRule
from vkbottle.tools.dev_tools.mini_types.bot.message import MessageMin
from typing import Callable, Any

LabeledMessageHandler = Callable[..., Callable[[MessageMin], Any]]


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
