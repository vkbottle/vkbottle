import typing
from vkbottle.api.api.util.token import AbstractTokenGenerator
from vkbottle.utils.logger import logger
from vkbottle.utils.exceptions import TokenGeneratorError


class TokenSchema:
    account = None
    ads = None
    appwidgets = None
    apps = None
    auth = None
    board = None
    database = None
    docs = None
    fave = None
    friends = None
    gifts = None
    groups = None
    leads = None
    likes = None
    market = None
    messages = None
    newsfeed = None
    notes = None
    notifications = None
    orders = None
    pages = None
    photos = None
    polls = None
    prettycards = None
    search = None
    secure = None
    stats = None
    status = None
    storage = None
    stories = None
    streaming = None
    users = None
    utils = None
    video = None
    wall = None
    widgets = None

    def __init__(self, **schema: typing.Dict[str, AbstractTokenGenerator]):
        for methods, generator in schema.items():
            setattr(self, methods, generator)

    def get_generator(self, *args, **kwargs) -> AbstractTokenGenerator:
        method = getattr(self, kwargs.get("method").split(".")[0].lower())
        if not method:
            if kwargs.get("throw_errors"):
                raise TokenGeneratorError(
                    f"Token Generator for method {method} is not assigned"
                )
            logger.error(f"Token Generator for method {method} is not assigned")
        return method

    def __repr__(self):
        return f"<TokenSchema {self.__class__.__qualname__}>"
