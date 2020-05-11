# Generated with love
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class UtilsCheckLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, url: str) -> responses.utils.CheckLink:
        """ utils.checkLink
        From Vk Docs: Checks whether a link is blocked in VK.
        Access from user, group, service token(s)
        :param url: Link to check (e.g., 'http://google.com').
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "utils.checkLink", params, response_model=responses.utils.CheckLinkModel
        )


class UtilsDeleteFromLastShortened(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, key: str) -> responses.ok_response.OkResponse:
        """ utils.deleteFromLastShortened
        From Vk Docs: Deletes shortened link from user's list.
        Access from user token(s)
        :param key: Link key (characters after vk.cc/).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "utils.deleteFromLastShortened",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class UtilsGetLastShortenedLinks(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, count: int = None, offset: int = None
    ) -> responses.utils.GetLastShortenedLinks:
        """ utils.getLastShortenedLinks
        From Vk Docs: Returns a list of user's shortened links.
        Access from user token(s)
        :param count: Number of links to return.
        :param offset: Offset needed to return a specific subset of links.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "utils.getLastShortenedLinks",
            params,
            response_model=responses.utils.GetLastShortenedLinksModel,
        )


class UtilsGetLinkStats(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        key: str,
        source: str = None,
        access_key: str = None,
        interval: str = None,
        intervals_count: int = None,
        extended: bool = None,
    ) -> responses.utils.GetLinkStats:
        """ utils.getLinkStats
        From Vk Docs: Returns stats data for shortened link.
        Access from user, group, service token(s)
        :param key: Link key (characters after vk.cc/).
        :param source: Source of scope
        :param access_key: Access key for private link stats.
        :param interval: Interval.
        :param intervals_count: Number of intervals to return.
        :param extended: 1 — to return extended stats data (sex, age, geo). 0 — to return views number only.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "utils.getLinkStats",
            params,
            response_model=responses.utils.GetLinkStatsModel,
        )


class UtilsGetServerTime(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self,) -> responses.utils.GetServerTime:
        """ utils.getServerTime
        From Vk Docs: Returns the current time of the VK server.
        Access from user, group, service token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "utils.getServerTime",
            params,
            response_model=responses.utils.GetServerTimeModel,
        )


class UtilsGetShortLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self, url: str, private: bool = None
    ) -> responses.utils.GetShortLink:
        """ utils.getShortLink
        From Vk Docs: Allows to receive a link shortened via vk.cc.
        Access from user, group, service token(s)
        :param url: URL to be shortened.
        :param private: 1 — private stats, 0 — public stats.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "utils.getShortLink",
            params,
            response_model=responses.utils.GetShortLinkModel,
        )


class UtilsResolveScreenName(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, screen_name: str) -> responses.utils.ResolveScreenName:
        """ utils.resolveScreenName
        From Vk Docs: Detects a type of object (e.g., user, community, application) and its ID by screen name.
        Access from user, group, service token(s)
        :param screen_name: Screen name of the user, community (e.g., 'apiclub,' 'andrew', or 'rules_of_war'), or application.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "utils.resolveScreenName",
            params,
            response_model=responses.utils.ResolveScreenNameModel,
        )


class Utils:
    def __init__(self, request):
        self.check_link = UtilsCheckLink(request)
        self.delete_from_last_shortened = UtilsDeleteFromLastShortened(request)
        self.get_last_shortened_links = UtilsGetLastShortenedLinks(request)
        self.get_link_stats = UtilsGetLinkStats(request)
        self.get_server_time = UtilsGetServerTime(request)
        self.get_short_link = UtilsGetShortLink(request)
        self.resolve_screen_name = UtilsResolveScreenName(request)
