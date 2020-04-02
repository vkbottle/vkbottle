# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class StoriesBanOwner(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owners_ids: typing.List):
        """ stories.banOwner
        From Vk Docs: Allows to hide stories from chosen sources from current user's feed.
        Access from user token(s)
        :param owners_ids: List of sources IDs
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.banOwner", params)


class StoriesDelete(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, owner_id: int, story_id: int):
        """ stories.delete
        From Vk Docs: Allows to delete story.
        Access from user, group token(s)
        :param owner_id: Story owner's ID. Current user id is used by default.
        :param story_id: Story ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.delete", params)


class StoriesGet(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, owner_id: int, extended: bool):
        """ stories.get
        From Vk Docs: Returns stories available for current user.
        Access from user, group token(s)
        :param owner_id: Owner ID.
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.get", params)


class StoriesGetBanned(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, extended: bool, fields: typing.List):
        """ stories.getBanned
        From Vk Docs: Returns list of sources hidden from current user's feed.
        Access from user token(s)
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.getBanned", params)


class StoriesGetById(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, stories: typing.List, extended: bool, fields: typing.List):
        """ stories.getById
        From Vk Docs: Returns story by its ID.
        Access from user, group token(s)
        :param stories: Stories IDs separated by commas. Use format {owner_id}+'_'+{story_id}, for example, 12345_54331.
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.getById", params)


class StoriesGetPhotoUploadServer(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        add_to_news: bool,
        user_ids: typing.List,
        reply_to_story: str,
        link_text: str,
        link_url: str,
        group_id: int,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.getPhotoUploadServer", params)


class StoriesGetReplies(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        owner_id: int,
        story_id: int,
        access_key: str,
        extended: bool,
        fields: typing.List,
    ):
        """ stories.getReplies
        From Vk Docs: Returns replies to the story.
        Access from user, group token(s)
        :param owner_id: Story owner ID.
        :param story_id: Story ID.
        :param access_key: Access key for the private object.
        :param extended: '1' — to return additional fields for users and communities. Default value is 0.
        :param fields: Additional fields to return
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.getReplies", params)


class StoriesGetStats(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, owner_id: int, story_id: int):
        """ stories.getStats
        From Vk Docs: Returns stories available for current user.
        Access from user, group token(s)
        :param owner_id: Story owner ID. 
        :param story_id: Story ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.getStats", params)


class StoriesGetVideoUploadServer(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        add_to_news: bool,
        user_ids: typing.List,
        reply_to_story: str,
        link_text: str,
        link_url: str,
        group_id: int,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.getVideoUploadServer", params)


class StoriesGetViewers(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, owner_id: int, story_id: int, count: int, offset: int, extended: bool
    ):
        """ stories.getViewers
        From Vk Docs: Returns a list of story viewers.
        Access from user, group token(s)
        :param owner_id: Story owner ID.
        :param story_id: Story ID.
        :param count: Maximum number of results.
        :param offset: Offset needed to return a specific subset of results.
        :param extended: '1' — to return detailed information about photos
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.getViewers", params)


class StoriesHideAllReplies(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, owner_id: int, group_id: int):
        """ stories.hideAllReplies
        From Vk Docs: Hides all replies in the last 24 hours from the user to current user's stories.
        Access from user, group token(s)
        :param owner_id: ID of the user whose replies should be hidden.
        :param group_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.hideAllReplies", params)


class StoriesHideReply(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, owner_id: int, story_id: int):
        """ stories.hideReply
        From Vk Docs: Hides the reply to the current user's story.
        Access from user, group token(s)
        :param owner_id: ID of the user whose replies should be hidden.
        :param story_id: Story ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.hideReply", params)


class StoriesUnbanOwner(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owners_ids: typing.List):
        """ stories.unbanOwner
        From Vk Docs: Allows to show stories from hidden sources in current user's feed.
        Access from user token(s)
        :param owners_ids: List of hidden sources to show stories from.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("stories.unbanOwner", params)


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
