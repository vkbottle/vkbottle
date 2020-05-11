# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class NotificationsGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        count: int = None,
        start_from: str = None,
        filters: typing.List = None,
        start_time: int = None,
        end_time: int = None,
    ) -> responses.notifications.Get:
        """ notifications.get
        From Vk Docs: Returns a list of notifications about other users' feedback to the current user's wall posts.
        Access from user token(s)
        :param count: Number of notifications to return.
        :param start_from: 
        :param filters: Type of notifications to return: 'wall' — wall posts, 'mentions' — mentions in wall posts, comments, or topics, 'comments' — comments to wall posts, photos, and videos, 'likes' — likes, 'reposted' — wall posts that are copied from the current user's wall, 'followers' — new followers, 'friends' — accepted friend requests
        :param start_time: Earliest timestamp (in Unix time) of a notification to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a notification to return. By default, the current time.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notifications.get", params, response_model=responses.notifications.GetModel
        )


class NotificationsMarkAsViewed(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self,) -> responses.notifications.MarkAsViewed:
        """ notifications.markAsViewed
        From Vk Docs: Resets the counter of new notifications about other users' feedback to the current user's wall posts.
        Access from user token(s)
        
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notifications.markAsViewed",
            params,
            response_model=responses.notifications.MarkAsViewedModel,
        )


class NotificationsSendMessage(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        user_ids: typing.List,
        message: str,
        fragment: str = None,
        group_id: int = None,
    ) -> responses.notifications.SendMessage:
        """ notifications.sendMessage
        From Vk Docs: 
        Access from user, service token(s)
        :param user_ids: 
        :param message: 
        :param fragment: 
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "notifications.sendMessage",
            params,
            response_model=responses.notifications.SendMessageModel,
        )


class Notifications:
    def __init__(self, request):
        self.get = NotificationsGet(request)
        self.mark_as_viewed = NotificationsMarkAsViewed(request)
        self.send_message = NotificationsSendMessage(request)
