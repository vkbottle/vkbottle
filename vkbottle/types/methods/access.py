from enum import Enum


class APIAccessibility(Enum):
    USER = "user"
    SERVICE = "service"
    GROUP = "group"
    OPEN = "open"
    VKME = "vkme"
    COVID = "covid"
