from enum import Enum


class JoinType(Enum):
    join = "join"
    unsure = "unsure"
    accepted = "accepted"
    approved = "approved"
    request = "request"
