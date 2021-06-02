"""
App authorization scope constants
Documentation: vk.com/dev/permissions
"""

from enum import IntEnum


class UserScope(IntEnum):
    NOTIFY = 2 ** 0
    FRIENDS = 2 ** 1
    PHOTOS = 2 ** 2
    AUDIO = 2 ** 3
    VIDEO = 2 ** 4
    STORIES = 2 ** 6
    PAGES = 2 ** 7
    ADD_LINK = 2 ** 8
    STATUS = 2 ** 10
    NOTES = 2 ** 11
    MESSAGES = 2 ** 12
    WALL = 2 ** 13
    ADS = 2 ** 15
    OFFLINE = 2 ** 16
    DOCS = 2 ** 17
    GROUPS = 2 ** 18
    NOTIFICATIONS = 2 ** 19
    STATS = 2 ** 20
    EMAIL = 2 ** 22
    MARKET = 2 ** 27


class GroupScope(IntEnum):
    STORIES = 2 ** 0
    PHOTOS = 2 ** 2
    APP_WIDGET = 2 ** 6
    MESSAGES = 2 ** 12
    DOCS = 2 ** 17
    MANAGE = 2 ** 18
