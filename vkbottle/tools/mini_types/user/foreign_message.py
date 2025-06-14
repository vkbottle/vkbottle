from typing import Any, List, Optional

import pydantic

from vkbottle.tools.mini_types.base.foreign_message import BaseForeignMessageMin


def _foreign_messages(cls: Any, values: Any) -> Any:  # noqa: ARG001
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
    user_id: Optional[int] = None
    reply_message: Optional["ForeignMessageMin"] = None
    fwd_messages: Optional[List["ForeignMessageMin"]] = pydantic.Field(
        default_factory=list["ForeignMessageMin"],
    )

    __foreign_messages = pydantic.model_validator(mode="after")(_foreign_messages)

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == self.user_id if (self.mention and self.user_id) else False


ForeignMessageMin.model_rebuild()


__all__ = ("ForeignMessageMin",)
