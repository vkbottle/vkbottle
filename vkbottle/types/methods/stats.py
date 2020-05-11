# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StatsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int = None,
        app_id: int = None,
        timestamp_from: int = None,
        timestamp_to: int = None,
        interval: str = None,
        intervals_count: int = None,
        filters: typing.List = None,
        stats_groups: typing.List = None,
        extended: bool = None,
    ) -> responses.stats.Get:
        """ stats.get
        From Vk Docs: Returns statistics of a community or an application.
        Access from user token(s)
        :param group_id: Community ID.
        :param app_id: Application ID.
        :param timestamp_from: 
        :param timestamp_to: 
        :param interval: 
        :param intervals_count: 
        :param filters: 
        :param stats_groups: 
        :param extended: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stats.get", params, response_model=responses.stats.GetModel
        )


class StatsGetPostReach(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: str, post_id: int
    ) -> responses.stats.GetPostReach:
        """ stats.getPostReach
        From Vk Docs: Returns stats for a wall post.
        Access from user token(s)
        :param owner_id: post owner community id. Specify with "-" sign.
        :param post_id: wall post id. Note that stats are available only for '300' last (newest) posts on a community wall.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stats.getPostReach",
            params,
            response_model=responses.stats.GetPostReachModel,
        )


class StatsTrackVisitor(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, id: str) -> responses.ok_response.OkResponse:
        """ stats.trackVisitor
        From Vk Docs: 
        Access from user token(s)
        :param id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stats.trackVisitor",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class Stats:
    def __init__(self, request):
        self.get = StatsGet(request)
        self.get_post_reach = StatsGetPostReach(request)
        self.track_visitor = StatsTrackVisitor(request)
