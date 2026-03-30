from typing import Any

import pydantic
from vkbottle_types.objects import ClientInfoForBots

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
        foreign_message.group_id = values.group_id
        foreign_message.client_info = values.client_info

    return values


class ForeignMessageMin(BaseForeignMessageMin):
    group_id: int | None = None
    client_info: ClientInfoForBots | None = None
    reply_message: "ForeignMessageMin | None" = None
    fwd_messages: list["ForeignMessageMin"] | None = pydantic.Field(  # type: ignore
        default_factory=list["ForeignMessageMin"],
    )

    __foreign_messages = pydantic.model_validator(mode="after")(_foreign_messages)

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == -self.group_id if (self.mention and self.group_id) else False


ForeignMessageMin.model_rebuild()


__all__ = ("ForeignMessageMin",)
