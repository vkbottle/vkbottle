from vkbottle.api.api.request import Request


class BaseMethod:
    def __init__(self, request: Request):
        self.request: Request = request
