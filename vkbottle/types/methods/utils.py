# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class UtilsCheckLink(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, url: str):
        """ utils.checkLink
        From Vk Docs: Checks whether a link is blocked in VK.
        Access from user, group, service token(s)
        :param url: Link to check (e.g., 'http://google.com').
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("utils.checkLink", params)


class UtilsDeleteFromLastShortened(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, key: str):
        """ utils.deleteFromLastShortened
        From Vk Docs: Deletes shortened link from user's list.
        Access from user token(s)
        :param key: Link key (characters after vk.cc/).
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("utils.deleteFromLastShortened", params)


class UtilsGetLastShortenedLinks(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, count: int, offset: int):
        """ utils.getLastShortenedLinks
        From Vk Docs: Returns a list of user's shortened links.
        Access from user token(s)
        :param count: Number of links to return.
        :param offset: Offset needed to return a specific subset of links.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("utils.getLastShortenedLinks", params)


class UtilsGetLinkStats(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        key: str,
        source: str,
        access_key: str,
        interval: str,
        intervals_count: int,
        extended: bool,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("utils.getLinkStats", params)


class UtilsGetServerTime(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self,):
        """ utils.getServerTime
        From Vk Docs: Returns the current time of the VK server.
        Access from user, group, service token(s)
        
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("utils.getServerTime", params)


class UtilsGetShortLink(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, url: str, private: bool):
        """ utils.getShortLink
        From Vk Docs: Allows to receive a link shortened via vk.cc.
        Access from user, group, service token(s)
        :param url: URL to be shortened.
        :param private: 1 — private stats, 0 — public stats.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("utils.getShortLink", params)


class UtilsResolveScreenName(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
        APIAccessibility.SERVICE,
    ]

    async def __call__(self, screen_name: str):
        """ utils.resolveScreenName
        From Vk Docs: Detects a type of object (e.g., user, community, application) and its ID by screen name.
        Access from user, group, service token(s)
        :param screen_name: Screen name of the user, community (e.g., 'apiclub,' 'andrew', or 'rules_of_war'), or application.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("utils.resolveScreenName", params)


class Utils:
    def __init__(self, request):
        self.check_link = UtilsCheckLink(request)
        self.delete_from_last_shortened = UtilsDeleteFromLastShortened(request)
        self.get_last_shortened_links = UtilsGetLastShortenedLinks(request)
        self.get_link_stats = UtilsGetLinkStats(request)
        self.get_server_time = UtilsGetServerTime(request)
        self.get_short_link = UtilsGetShortLink(request)
        self.resolve_screen_name = UtilsResolveScreenName(request)
