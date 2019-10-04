from enum import IntEnum


class AdminLevel(IntEnum):
    no_role = 0
    moderator = 1
    editor = 2
    administrator = 3
