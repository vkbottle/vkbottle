import typing
from vkbottle.http import HTTPRequest
from vkbottle.utils import ContextInstanceMixin

from vkbottle.types.methods import *
from .request import Request
from .builtin import AbstractTokenGenerator, ConsistentTokenGenerator, GENERATORS


class API(ContextInstanceMixin):
    def __init__(
        self,
        tokens: typing.List[str] = None,
        generator: typing.Union[str] = "consistent",
        throw_errors: bool = True,
    ):
        self.token_generator: AbstractTokenGenerator = GENERATORS.get(
            generator, ConsistentTokenGenerator
        )(tokens)
        self._http = HTTPRequest()
        self.throw_errors: bool = throw_errors

        # VK Api Methods
        self.account = Account(self.api)
        self.ads = Ads(self.api)
        self.appwidgets = Appwidgets(self.api)
        self.apps = Apps(self.api)
        self.auth = Auth(self.api)
        self.board = Board(self.api)
        self.database = Database(self.api)
        self.docs = Docs(self.api)
        self.fave = Fave(self.api)
        self.friends = Friends(self.api)
        self.gifts = Gifts(self.api)
        self.groups = Groups(self.api)
        self.leads = Leads(self.api)
        self.likes = Likes(self.api)
        self.market = Market(self.api)
        self.messages = Messages(self.api)
        self.newsfeed = Newsfeed(self.api)
        self.notes = Notes(self.api)
        self.notifications = Notifications(self.api)
        self.orders = Orders(self.api)
        self.pages = Pages(self.api)
        self.photos = Photos(self.api)
        self.polls = Polls(self.api)
        self.prettycards = Prettycards(self.api)
        self.search = Search(self.api)
        self.secure = Secure(self.api)
        self.stats = Stats(self.api)
        self.status = Status(self.api)
        self.storage = Storage(self.api)
        self.stories = Stories(self.api)
        self.streaming = Streaming(self.api)
        self.users = Users(self.api)
        self.utils = Utils(self.api)
        self.video = Video(self.api)
        self.wall = Wall(self.api)
        self.widgets = Widgets(self.api)

    def api(self, *args, **kwargs):
        request = Request(self.token_generator)
        return request(*args, **kwargs)

    async def request(
        self,
        method: str,
        params: dict,
        throw_errors: typing.Optional[bool] = None,
        response_model=None,
        raw_response: bool = False,
    ):
        return await self.api(
            method,
            params,
            throw_errors=throw_errors,
            response_model=response_model,
            raw_response=raw_response,
        )


class UserApi(API, ContextInstanceMixin):
    pass


class Api(API, ContextInstanceMixin):
    pass
