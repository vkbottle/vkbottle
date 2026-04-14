from typing import Any

import pydantic

from vkbottle.tools.mini_types.base.foreign_message import BaseForeignMessageMin


def _foreign_messages(values: Any) -> Any:
    foreign_messages = []

    if values.fwd_messages:
        foreign_messages.extend(values.fwd_messages)

    if values.reply_message:
        foreign_messages.append(values.reply_message)

    for foreign_message in foreign_messages:
        foreign_message.unprepared_ctx_api = values.unprepared_ctx_api
        foreign_message.replace_mention = values.replace_mention
        foreign_message.user_id = values.user_id

    return values


class ForeignMessageMin(BaseForeignMessageMin):
    user_id: int | None = None
    reply_message: "ForeignMessageMin | None" = None
    fwd_messages: list["ForeignMessageMin"] | None = pydantic.Field(  # type: ignore
        default_factory=list["ForeignMessageMin"],
    )

    @pydantic.model_validator(mode="after")
    def foreign_messages_model(self) -> "ForeignMessageMin":
        return _foreign_messages(self)

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == self.user_id if (self.mention and self.user_id) else False


ForeignMessageMin.object_build(locals())


__all__ = ("ForeignMessageMin",)
