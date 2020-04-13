import typing
from vkbottle.framework.framework.rule import UserLongPollEventRule
from vkbottle.types.user_longpoll import Message

ADDITIONAL_FIELDS = ("peer_id", "timestamp", "text", "info", "attachments", "random_id")


class Handler:
    def __init__(self):
        self.rules: typing.List[UserLongPollEventRule] = list()

    def concatenate(self, other: "Handler"):
        self.rules += other.rules

    def message_flag_change(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(1, *rules)
            rule.create(
                func,
                {
                    "name": "message_flag_change",
                    "data": ["message_id", "flags", *ADDITIONAL_FIELDS],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_flag_set(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(2, *rules)
            rule.create(
                func,
                {
                    "name": "message_flag_set",
                    "data": ["message_id", "mask", *ADDITIONAL_FIELDS],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_flag_remove(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(3, *rules)
            rule.create(
                func,
                {
                    "name": "message_flag_remove",
                    "data": ["message_id", "mask", *ADDITIONAL_FIELDS],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_new(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(4, *rules)
            rule.create(
                func,
                {
                    "name": "message_new",
                    "data": ["message_id", "flags", *ADDITIONAL_FIELDS],
                    "dataclass": Message,
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_edit(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(5, *rules)
            rule.create(
                func,
                {
                    "name": "message_edit",
                    "data": [
                        "message_id",
                        "mask",
                        "peer_id",
                        "timestamp",
                        "new_text",
                        *ADDITIONAL_FIELDS,
                    ],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_read_in(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(6, *rules)
            rule.create(
                func, {"name": "message_read_in", "data": ["peer_id", "local_id",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_read_out(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(7, *rules)
            rule.create(
                func, {"name": "message_read_out", "data": ["peer_id", "local_id",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def friend_online(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(8, *rules)
            rule.create(
                func,
                {"name": "friend_online", "data": ["user_id", "extra", "timestamp",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def friend_offline(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(9, *rules)
            rule.create(
                func,
                {"name": "friend_offline", "data": ["user_id", "flags", "timestamp",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_flag_change(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(11, *rules)
            rule.create(
                func, {"name": "chat_flag_change", "data": ["peer_id", "flags",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_flag_set(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(12, *rules)
            rule.create(
                func, {"name": "chat_flag_set", "data": ["peer_id", "mask",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_flag_remove(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(10, *rules)
            rule.create(
                func, {"name": "chat_flag_remove", "data": ["peer_id", "mask",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_remove(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(13, *rules)
            rule.create(
                func, {"name": "chat_remove", "data": ["peer_id", "local_id",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_restore(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(14, *rules)
            rule.create(
                func, {"name": "chat_restore", "data": ["peer_id", "local_id",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_edit(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(51, *rules)
            rule.create(
                func, {"name": "chat_edit", "data": ["chat_id", "self",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_info_edit(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(52, *rules)
            rule.create(
                func,
                {"name": "chat_info_edit", "data": ["type_id", "peer_id", "info",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def message_typing_state(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(61, *rules)
            rule.create(
                func, {"name": "message_typing_state", "data": ["user_id", "flags",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_typing_state(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(62, *rules)
            rule.create(
                func, {"name": "chat_typing_state", "data": ["user_id", "chat_id",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_typing_states(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(63, *rules)
            rule.create(
                func,
                {
                    "name": "chat_typing_states",
                    "data": ["user_ids", "peer_id", "total_count", "ts",],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def chat_voice_message_states(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(64, *rules)
            rule.create(
                func,
                {
                    "name": "chat_voice_message_states",
                    "data": ["user_ids", "peer_id", "total_count", "ts",],
                },
            )
            self.rules.append(rule)
            return func

        return decorator

    def call(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(70, *rules)
            rule.create(
                func, {"name": "call", "data": ["user_id", "call_id",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def left_counter(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(80, *rules)
            rule.create(
                func, {"name": "left_counter", "data": ["counter", "null",],},
            )
            self.rules.append(rule)
            return func

        return decorator

    def notifications_settings_changed(self, *rules):
        def decorator(func):
            rule = UserLongPollEventRule(114, *rules)
            rule.create(
                func,
                {
                    "name": "notifications_settings_changed",
                    "data": ["peer_id", "sound", "disabled_until",],
                },
            )
            self.rules.append(rule)
            return func

        return decorator
