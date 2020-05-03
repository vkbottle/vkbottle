import typing

if typing.TYPE_CHECKING:
    from vkbottle.api.api.request import Request


class BaseMethod:
    def __init__(self, request: "Request"):
        self.request: "Request" = request

    def __repr__(self):
        return f"<Method {self.__class__.__qualname__}>"
