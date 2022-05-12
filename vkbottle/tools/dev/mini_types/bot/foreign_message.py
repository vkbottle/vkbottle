from typing import List, Optional

from pydantic import root_validator
from vkbottle_types.objects import ClientInfoForBots

from ..base.foreign_message import BaseForeignMessageMin


class ForeignMessageMin(BaseForeignMessageMin):
    group_id: Optional[int] = None
    client_info: Optional["ClientInfoForBots"] = None
    reply_message: Optional["ForeignMessageMin"] = None
    fwd_messages: Optional[List["ForeignMessageMin"]] = []

    @root_validator
    def __foreign_messages(cls, values):
        foreign_messages = []
        if values.get("fwd_messages"):
            foreign_messages.extend(values["fwd_messages"])
        if values.get("reply_message"):
            foreign_messages.append(values["reply_message"])
        for foreign_message in foreign_messages:
            foreign_message.unprepared_ctx_api = values["unprepared_ctx_api"]
            foreign_message.replace_mention = values["replace_mention"]
            foreign_message.group_id = values["group_id"]
            foreign_message.client_info = values["client_info"]
        return values

    @property
    def is_mentioned(self) -> bool:
        return self.mention.id == -self.group_id if (self.mention and self.group_id) else False


ForeignMessageMin.update_forward_refs()
