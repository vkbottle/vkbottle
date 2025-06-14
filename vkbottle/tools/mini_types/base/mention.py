import re
from typing import Any

import pydantic

MENTION_PATTERN = re.compile(r"^\[(?P<type>club|public|id)(?P<id>\d*)\|(?P<text>.+)\],?\s?")


class Mention(pydantic.BaseModel):
    """Mention object

    :param id: Identifier of the user that was mentioned (negative if it's a group)
    :param text: Mention text
    """

    id: int
    text: str


def replace_mention_validator(cls: Any, values: Any) -> Any:  # noqa: ARG001
    if not values.replace_mention:
        return values

    message_text = values.text
    if not message_text:
        return values

    match = MENTION_PATTERN.search(message_text)
    if not match:
        return values

    values.text = message_text.replace(match.group(0), "", 1)
    mention_id = int(match.group("id"))
    if match.group("type") in ("club", "public"):
        mention_id = -mention_id

    values._mention = Mention(id=mention_id, text=match.group("text"))
    return values


__all__ = ("Mention", "replace_mention_validator")
