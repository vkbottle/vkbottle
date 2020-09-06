from .abc import ABCBotLabeler, LabeledMessageHandler
from vkbottle.dispatch.rules import ABCRule
from vkbottle.dispatch.views import MessageView
from vkbottle.dispatch.handlers import FromFuncHandler


class BotLabeler(ABCBotLabeler):
    message_view = MessageView()

    def message(
        self, *rules: "ABCRule", blocking: bool = False, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(FromFuncHandler(func, *rules, blocking=blocking))
            return func

        return decorator

    def chat_message(
        self, *rules: "ABCRule", blocking: bool = False, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(FromFuncHandler(func, *rules, blocking=blocking))
            return func

        return decorator

    def private_message(
        self, *rules: "ABCRule", blocking: bool = False, **custom_rules
    ) -> LabeledMessageHandler:
        def decorator(func):
            self.message_view.handlers.append(FromFuncHandler(func, *rules, blocking=blocking))
            return func

        return decorator
