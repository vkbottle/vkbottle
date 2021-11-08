from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Union

from vkbottle_types.events.user_events import RawUserEvent

if TYPE_CHECKING:
    from vkbottle.dispatch.rules import ABCRule
    from vkbottle.dispatch.views import ABCView
    from vkbottle.tools.dev.mini_types.user.message import MessageMin

    LabeledMessageHandler = Callable[..., Callable[["MessageMin"], Any]]
    LabeledHandler = Callable[..., Callable[[Any], Any]]


class ABCUserLabeler(ABC):
    @abstractmethod
    def message(self, *rules: "ABCRule", **custom_rules) -> "LabeledMessageHandler":
        pass

    @abstractmethod
    def chat_message(self, *rules: "ABCRule", **custom_rules) -> "LabeledMessageHandler":
        pass

    @abstractmethod
    def private_message(self, *rules: "ABCRule", **custom_rules) -> "LabeledMessageHandler":
        pass

    @abstractmethod
    def raw_event(
        self,
        event: Union[str, List[str]],
        dataclass: Callable = RawUserEvent,
        *rules: "ABCRule",
        **custom_rules,
    ) -> "LabeledHandler":
        pass

    @abstractmethod
    def views(self) -> Dict[str, "ABCView"]:
        pass

    @abstractmethod
    def load(self, labeler: Any):
        pass