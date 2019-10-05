from enum import IntEnum


class BlockReason(IntEnum):
    other = 0
    spam = 1
    verbal_abuse = 2
    strong_language = 3
    irrelevant_messages = 4
