import typing
from abc import ABC, abstractmethod

from vbml import Pattern

from vkbottle.framework.framework.rule import (
    VBMLRule,
    ChatActionRule,
    AbstractMessageRule,
)
from .events import ABCEvents
from .message import ABCMessageHandler


class ABCHandler(ABC):
    message: ABCMessageHandler
    chat_message: ABCMessageHandler
    message_handler: ABCMessageHandler
    event: ABCEvents
    _pre_p: typing.Optional[typing.Callable] = None
    group_id: typing.Optional[int] = None
    user_id: typing.Optional[int] = None
    message_rules: typing.List[typing.List[AbstractMessageRule]]

    @abstractmethod
    def concatenate(self, handler: "ABCHandler"):
        pass

    @abstractmethod
    def dispatch(
        self, get_current_rest: typing.Callable[[], typing.Awaitable[dict]] = None
    ) -> None:
        pass

    def chat_action(
        self, type_: typing.Union[str, typing.List[str]], rules: dict = None
    ):
        """
        Special express processor of chat actions (https://vk.com/dev/objects/message - action object)
        :param type_: action name
        :param rules:
        """

        def decorator(func):
            rule = ChatActionRule(type_, rules=rules)
            self.chat_message.add_rules([rule], func)
            return func

        return decorator

    def chat_mention(self):
        def decorator(func):
            pattern = Pattern(pattern=r"\[(club|public){}\|.*?]".format(self.group_id))
            rule = VBMLRule(pattern)
            self.chat_message.add_rules([rule], func)
            return func

        return decorator

    def chat_invite(self):
        def decorator(func):
            rule = ChatActionRule("chat_invite_user", {"member_id": -self.group_id})
            self.chat_message.add_rules([rule], func)
            return func

        return decorator

    @property
    def pre_p(self):
        return self._pre_p

    @property
    def instance_id(self) -> int:
        if self.group_id:
            return -self.group_id
        return self.user_id

    def pre_process(self):
        def decorator(func):
            self._pre_p = func
            return func

        return decorator

    def __repr__(self):
        return (
            f"MESSAGE HANDLERS:              {len(self.message.rules) + len(self.message_handler.rules)}\n"
            f"CHAT-MESSAGE HANDLERS:         {len(self.chat_message.rules) + len(self.message_handler.rules)}\n"
            f"EVENT HANDLERS:                {len(self.event.rules)}\n"
        )
