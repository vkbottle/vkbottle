from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule, bot
from vkbottle.dispatch.views import MessageView, ABCView, RawEventView, HandlerBasement
from .abc import ABCBotLabeler, LabeledMessageHandler, LabeledHandler
from typing import Dict, Union, List, Callable


class BotLabeler(ABCBotLabeler):
    def __init__(self):
        self.message_view = MessageView()
        self.raw_event_view = RawEventView()

    def message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func, *rules, *self.get_custom_rules(custom_rules), blocking=blocking
                )
            )
            return func

        return decorator

    def chat_message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    bot.PeerRule(True),
                    *rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def private_message(
        self, *rules: "ABCRule", blocking: bool = True, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(
                FromFuncHandler(
                    func,
                    bot.PeerRule(False),
                    *rules,
                    *self.get_custom_rules(custom_rules),
                    blocking=blocking,
                )
            )
            return func

        return decorator

    def raw_event(
        self,
        event: Union[str, List[str]],
        dataclass: Callable = dict,
        *rules: "ABCRule",
        **custom_rules,
    ) -> LabeledHandler:
        if not isinstance(event, list):
            event = [event]

        def decorator(func):
            for e in event:
                self.raw_event_view.handlers[e] = HandlerBasement(
                    dataclass, FromFuncHandler(func, *rules, *self.get_custom_rules(custom_rules)),
                )
            return func

        return decorator

    def load(self, labeler: "BotLabeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        self.message_view.middlewares.extend(labeler.message_view.middlewares)
        self.raw_event_view.handlers.update(labeler.raw_event_view.handlers)
        self.raw_event_view.middlewares.extend(labeler.raw_event_view.middlewares)

    def views(self) -> Dict[str, "ABCView"]:
        return {"message": self.message_view, "raw": self.raw_event_view}
