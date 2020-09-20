from .abc import ABCBotLabeler, LabeledMessageHandler
from vkbottle.dispatch.rules import ABCRule, bot
from vkbottle.dispatch.views import MessageView
from vkbottle.dispatch.handlers import FromFuncHandler


class BotLabeler(ABCBotLabeler):
    message_view = MessageView()

    def message(
        self, *rules: "ABCRule", blocking: bool = False, **custom_rules
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
        self, *rules: "ABCRule", blocking: bool = False, **custom_rules
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
        self, *rules: "ABCRule", blocking: bool = False, **custom_rules
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

    def load(self, labeler: "BotLabeler"):
        self.message_view.handlers.extend(labeler.message_view.handlers)
        self.message_view.middlewares.extend(labeler.message_view.middlewares)
