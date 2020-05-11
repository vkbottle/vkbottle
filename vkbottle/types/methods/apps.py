# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class AppsDeleteAppRequests(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self,) -> responses.ok_response.OkResponse:
        """ apps.deleteAppRequests
        From Vk Docs: Deletes all request notifications from the current app.
        Access from user token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.deleteAppRequests",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class AppsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        app_id: int = None,
        app_ids: typing.List = None,
        platform: str = None,
        extended: bool = None,
        return_friends: bool = None,
        fields: typing.List = None,
        name_case: str = None,
    ) -> responses.apps.Get:
        """ apps.get
        From Vk Docs: Returns applications data.
        Access from user, service token(s)
        :param app_id: Application ID
        :param app_ids: List of application ID
        :param platform: platform. Possible values: *'ios' — iOS,, *'android' — Android,, *'winphone' — Windows Phone,, *'web' — приложения на vk.com. By default: 'web'.
        :param extended: 
        :param return_friends: 
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate' (birthdate), 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'contacts', 'education', 'online', 'counters', 'relation', 'last_seen', 'activity', 'can_write_private_message', 'can_see_all_posts', 'can_post', 'universities', (only if return_friends - 1)
        :param name_case: Case for declension of user name and surname: 'nom' — nominative (default),, 'gen' — genitive,, 'dat' — dative,, 'acc' — accusative,, 'ins' — instrumental,, 'abl' — prepositional. (only if 'return_friends' = '1')
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.get", params, response_model=responses.apps.GetModel
        )


class AppsGetCatalog(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        count: int,
        sort: str = None,
        offset: int = None,
        platform: str = None,
        extended: bool = None,
        return_friends: bool = None,
        fields: typing.List = None,
        name_case: str = None,
        q: str = None,
        genre_id: int = None,
        filter: str = None,
    ) -> responses.apps.GetCatalog:
        """ apps.getCatalog
        From Vk Docs: Returns a list of applications (apps) available to users in the App Catalog.
        Access from user, service token(s)
        :param sort: Sort order: 'popular_today' — popular for one day (default), 'visitors' — by visitors number , 'create_date' — by creation date, 'growth_rate' — by growth rate, 'popular_week' — popular for one week
        :param offset: Offset required to return a specific subset of apps.
        :param count: Number of apps to return.
        :param platform: 
        :param extended: '1' — to return additional fields 'screenshots', 'MAU', 'catalog_position', and 'international'. If set, 'count' must be less than or equal to '100'. '0' — not to return additional fields (default).
        :param return_friends: 
        :param fields: 
        :param name_case: 
        :param q: Search query string.
        :param genre_id: 
        :param filter: 'installed' — to return list of installed apps (only for mobile platform).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.getCatalog", params, response_model=responses.apps.GetCatalogModel
        )


class AppsGetFriendsList(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        extended: bool = None,
        count: int = None,
        offset: int = None,
        type: str = None,
        fields: typing.List = None,
    ) -> responses.apps.GetFriendsList:
        """ apps.getFriendsList
        From Vk Docs: Creates friends list for requests and invites in current app.
        Access from user token(s)
        :param extended: 
        :param count: List size.
        :param offset: 
        :param type: List type. Possible values: * 'invite' — available for invites (don't play the game),, * 'request' — available for request (play the game). By default: 'invite'.
        :param fields: Additional profile fields, see [vk.com/dev/fields|description].
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.getFriendsList",
            params,
            response_model=responses.apps.GetFriendsListModel,
        )


class AppsGetLeaderboard(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, type: str, global_: bool = None, extended: bool = None
    ) -> responses.apps.GetLeaderboard:
        """ apps.getLeaderboard
        From Vk Docs: Returns players rating in the game.
        Access from user token(s)
        :param type: Leaderboard type. Possible values: *'level' — by level,, *'points' — by mission points,, *'score' — by score ().
        :param global: Rating type. Possible values: *'1' — global rating among all players,, *'0' — rating among user friends.
        :param extended: 1 — to return additional info about users
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.getLeaderboard",
            params,
            response_model=responses.apps.GetLeaderboardModel,
        )


class AppsGetScopes(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, type: str = None) -> responses.apps.GetScopes:
        """ apps.getScopes
        From Vk Docs: Returns scopes for auth
        Access from user token(s)
        :param type: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.getScopes", params, response_model=responses.apps.GetScopesModel
        )


class AppsGetScore(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int) -> responses.apps.GetScore:
        """ apps.getScore
        From Vk Docs: Returns user score in app
        Access from user token(s)
        :param user_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.getScore", params, response_model=responses.apps.GetScoreModel
        )


class AppsSendRequest(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        user_id: int,
        text: str = None,
        type: str = None,
        name: str = None,
        key: str = None,
        separate: bool = None,
    ) -> responses.apps.SendRequest:
        """ apps.sendRequest
        From Vk Docs: Sends a request to another user in an app that uses VK authorization.
        Access from user token(s)
        :param user_id: id of the user to send a request
        :param text: request text
        :param type: request type. Values: 'invite' – if the request is sent to a user who does not have the app installed,, 'request' – if a user has already installed the app
        :param name: 
        :param key: special string key to be sent with the request
        :param separate: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "apps.sendRequest", params, response_model=responses.apps.SendRequestModel
        )


class Apps:
    def __init__(self, request):
        self.delete_app_requests = AppsDeleteAppRequests(request)
        self.get = AppsGet(request)
        self.get_catalog = AppsGetCatalog(request)
        self.get_friends_list = AppsGetFriendsList(request)
        self.get_leaderboard = AppsGetLeaderboard(request)
        self.get_scopes = AppsGetScopes(request)
        self.get_score = AppsGetScore(request)
        self.send_request = AppsSendRequest(request)
