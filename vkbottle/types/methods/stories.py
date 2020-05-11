# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StoriesBanOwner(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owners_ids: typing.List
    ) -> responses.ok_response.OkResponse:
        """ stories.banOwner
        From Vk Docs: Allows to hide stories from chosen sources from current user's feed.
        Access from user token(s)
        :param owners_ids: List of sources IDs
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.banOwner",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class StoriesDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, owner_id: int, story_id: int
    ) -> responses.ok_response.OkResponse:
        """ stories.delete
        From Vk Docs: Allows to delete story.
        Access from user, group token(s)
        :param owner_id: Story owner's ID. Current user id is used by default.
        :param story_id: Story ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.delete",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class StoriesGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, owner_id: int = None, extended: bool = None
    ) -> responses.stories.Get:
        """ stories.get
        From Vk Docs: Returns stories available for current user.
        Access from user, group token(s)
        :param owner_id: Owner ID.
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.get", params, response_model=responses.stories.GetModel
        )


class StoriesGetBanned(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, extended: bool = None, fields: typing.List = None
    ) -> responses.stories.GetBanned:
        """ stories.getBanned
        From Vk Docs: Returns list of sources hidden from current user's feed.
        Access from user token(s)
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.getBanned", params, response_model=responses.stories.GetBannedModel
        )


class StoriesGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, stories: typing.List, extended: bool = None, fields: typing.List = None
    ) -> responses.stories.GetById:
        """ stories.getById
        From Vk Docs: Returns story by its ID.
        Access from user, group token(s)
        :param stories: Stories IDs separated by commas. Use format {owner_id}+'_'+{story_id}, for example, 12345_54331.
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.getById", params, response_model=responses.stories.GetByIdModel
        )


class StoriesGetPhotoUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        add_to_news: bool = None,
        user_ids: typing.List = None,
        reply_to_story: str = None,
        link_text: str = None,
        link_url: str = None,
        group_id: int = None,
    ) -> responses.stories.GetPhotoUploadServer:
        """ stories.getPhotoUploadServer
        From Vk Docs: Returns URL for uploading a story with photo.
        Access from user, group token(s)
        :param add_to_news: 1 — to add the story to friend's feed.
        :param user_ids: List of users IDs who can see the story.
        :param reply_to_story: ID of the story to reply with the current.
        :param link_text: Link text (for community's stories only).
        :param link_url: Link URL. Internal links on https://vk.com only.
        :param group_id: ID of the community to upload the story (should be verified or with the "fire" icon).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.getPhotoUploadServer",
            params,
            response_model=responses.stories.GetPhotoUploadServerModel,
        )


class StoriesGetReplies(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        owner_id: int,
        story_id: int,
        access_key: str = None,
        extended: bool = None,
        fields: typing.List = None,
    ) -> responses.stories.GetReplies:
        """ stories.getReplies
        From Vk Docs: Returns replies to the story.
        Access from user, group token(s)
        :param owner_id: Story owner ID.
        :param story_id: Story ID.
        :param access_key: Access key for the private object.
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.getReplies",
            params,
            response_model=responses.stories.GetRepliesModel,
        )


class StoriesGetStats(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, owner_id: int, story_id: int
    ) -> responses.stories.GetStats:
        """ stories.getStats
        From Vk Docs: Returns stories available for current user.
        Access from user, group token(s)
        :param owner_id: Story owner ID. 
        :param story_id: Story ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.getStats", params, response_model=responses.stories.GetStatsModel
        )


class StoriesGetVideoUploadServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        add_to_news: bool = None,
        user_ids: typing.List = None,
        reply_to_story: str = None,
        link_text: str = None,
        link_url: str = None,
        group_id: int = None,
    ) -> responses.stories.GetVideoUploadServer:
        """ stories.getVideoUploadServer
        From Vk Docs: Allows to receive URL for uploading story with video.
        Access from user, group token(s)
        :param add_to_news: 1 — to add the story to friend's feed.
        :param user_ids: List of users IDs who can see the story.
        :param reply_to_story: ID of the story to reply with the current.
        :param link_text: Link text (for community's stories only).
        :param link_url: Link URL. Internal links on https://vk.com only.
        :param group_id: ID of the community to upload the story (should be verified or with the "fire" icon).
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.getVideoUploadServer",
            params,
            response_model=responses.stories.GetVideoUploadServerModel,
        )


class StoriesGetViewers(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        owner_id: int,
        story_id: int,
        count: int = None,
        offset: int = None,
        extended: bool = None,
    ) -> responses.stories.GetViewers:
        """ stories.getViewers
        From Vk Docs: Returns a list of story viewers.
        Access from user, group token(s)
        :param owner_id: Story owner ID.
        :param story_id: Story ID.
        :param count: Maximum number of results.
        :param offset: Offset needed to return a specific subset of results.
        :param extended: '1' — to return detailed information about photos
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.getViewers",
            params,
            response_model=responses.stories.GetViewersModel,
        )


class StoriesHideAllReplies(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, owner_id: int, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ stories.hideAllReplies
        From Vk Docs: Hides all replies in the last 24 hours from the user to current user's stories.
        Access from user, group token(s)
        :param owner_id: ID of the user whose replies should be hidden.
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.hideAllReplies",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class StoriesHideReply(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, owner_id: int, story_id: int
    ) -> responses.ok_response.OkResponse:
        """ stories.hideReply
        From Vk Docs: Hides the reply to the current user's story.
        Access from user, group token(s)
        :param owner_id: ID of the user whose replies should be hidden.
        :param story_id: Story ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.hideReply",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class StoriesUnbanOwner(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owners_ids: typing.List
    ) -> responses.ok_response.OkResponse:
        """ stories.unbanOwner
        From Vk Docs: Allows to show stories from hidden sources in current user's feed.
        Access from user token(s)
        :param owners_ids: List of hidden sources to show stories from.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "stories.unbanOwner",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class Stories:
    def __init__(self, request):
        self.ban_owner = StoriesBanOwner(request)
        self.delete = StoriesDelete(request)
        self.get = StoriesGet(request)
        self.get_banned = StoriesGetBanned(request)
        self.get_by_id = StoriesGetById(request)
        self.get_photo_upload_server = StoriesGetPhotoUploadServer(request)
        self.get_replies = StoriesGetReplies(request)
        self.get_stats = StoriesGetStats(request)
        self.get_video_upload_server = StoriesGetVideoUploadServer(request)
        self.get_viewers = StoriesGetViewers(request)
        self.hide_all_replies = StoriesHideAllReplies(request)
        self.hide_reply = StoriesHideReply(request)
        self.unban_owner = StoriesUnbanOwner(request)
