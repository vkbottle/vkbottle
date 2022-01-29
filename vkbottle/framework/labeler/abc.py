from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Type, Union

if TYPE_CHECKING:
    from vkbottle.dispatch.rules import ABCRule
    from vkbottle.dispatch.views import ABCView
    from vkbottle.dispatch.views.abc import ABCMessageView, ABCRawEventView
    from vkbottle.tools.dev.mini_types.base.message import BaseMessageMin

    LabeledMessageHandler = Callable[..., Callable[["BaseMessageMin"], Any]]
    LabeledHandler = Callable[..., Callable[[Any], Any]]


class ABCLabeler(ABC):
    message_view: "ABCMessageView"
    raw_event_view: "ABCRawEventView"
    custom_rules: Dict[str, Type["ABCRule"]]
    auto_rules: List["ABCRule"]
    rule_config: Dict[str, Any]

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
        dataclass: Any,
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
