import typing
from vkbottle.http import HTTPRequest
from vkbottle.utils import ContextInstanceMixin

from vkbottle.types.methods import *
from .request import Request


def exception_handler(loop, context):
    pass


class ApiInstance(ContextInstanceMixin):
    def __init__(self, token: str, throw_errors: bool = True):
        self._token = token
        self._request = HTTPRequest()
        self.request = Request(self._token)
        self.throw_errors: bool = throw_errors

        # VK Api Methods
        self.account = Account(self.request)
        self.ads = Ads(self.request)
        self.appwidgets = Appwidgets(self.request)
        self.apps = Apps(self.request)
        self.auth = Auth(self.request)
        self.board = Board(self.request)
        self.database = Database(self.request)
        self.docs = Docs(self.request)
        self.fave = Fave(self.request)
        self.friends = Friends(self.request)
        self.gifts = Gifts(self.request)
        self.groups = Groups(self.request)
        self.leads = Leads(self.request)
        self.likes = Likes(self.request)
        self.market = Market(self.request)
        self.messages = Messages(self.request)
        self.newsfeed = Newsfeed(self.request)
        self.notes = Notes(self.request)
        self.notifications = Notifications(self.request)
        self.orders = Orders(self.request)
        self.pages = Pages(self.request)
        self.photos = Photos(self.request)
        self.polls = Polls(self.request)
        self.prettycards = Prettycards(self.request)
        self.search = Search(self.request)
        self.secure = Secure(self.request)
        self.stats = Stats(self.request)
        self.status = Status(self.request)
        self.storage = Storage(self.request)
        self.stories = Stories(self.request)
        self.streaming = Streaming(self.request)
        self.users = Users(self.request)
        self.utils = Utils(self.request)
        self.video = Video(self.request)
        self.wall = Wall(self.request)
        self.widgets = Widgets(self.request)

    async def request(
        self,
        method: str,
        params: dict,
        throw_errors: typing.Optional[bool] = None,
        response_model=None,
        raw_response: bool = False,
    ):
        return await self.request(
            method,
            params,
            throw_errors=throw_errors,
            response_model=response_model,
            raw_response=raw_response,
        )


class UserApi(ApiInstance, ContextInstanceMixin):
    pass


class Api(ApiInstance, ContextInstanceMixin):
    pass
