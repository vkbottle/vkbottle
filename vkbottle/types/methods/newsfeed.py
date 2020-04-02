# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class NewsfeedAddBan(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_ids: typing.List, group_ids: typing.List):
        """ newsfeed.addBan
        From Vk Docs: Prevents news from specified users and communities from appearing in the current user's newsfeed.
        Access from user token(s)
        :param user_ids: 
        :param group_ids: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.addBan", params)


class NewsfeedDeleteBan(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_ids: typing.List, group_ids: typing.List):
        """ newsfeed.deleteBan
        From Vk Docs: Allows news from previously banned users and communities to be shown in the current user's newsfeed.
        Access from user token(s)
        :param user_ids: 
        :param group_ids: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.deleteBan", params)


class NewsfeedDeleteList(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, list_id: int):
        """ newsfeed.deleteList
        From Vk Docs: 
        Access from user token(s)
        :param list_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.deleteList", params)


class NewsfeedGet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        filters: typing.List,
        return_banned: bool,
        start_time: int,
        end_time: int,
        max_photos: int,
        source_ids: str,
        start_from: str,
        count: int,
        fields: typing.List,
        section: str,
    ):
        """ newsfeed.get
        From Vk Docs: Returns data required to show newsfeed for the current user.
        Access from user token(s)
        :param filters: Filters to apply: 'post' — new wall posts, 'photo' — new photos, 'photo_tag' — new photo tags, 'wall_photo' — new wall photos, 'friend' — new friends, 'note' — new notes
        :param return_banned: '1' — to return news items from banned sources
        :param start_time: Earliest timestamp (in Unix time) of a news item to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a news item to return. By default, the current time.
        :param max_photos: Maximum number of photos to return. By default, '5'.
        :param source_ids: Sources to obtain news from, separated by commas. User IDs can be specified in formats '' or 'u' , where '' is the user's friend ID. Community IDs can be specified in formats '-' or 'g' , where '' is the community ID. If the parameter is not set, all of the user's friends and communities are returned, except for banned sources, which can be obtained with the [vk.com/dev/newsfeed.getBanned|newsfeed.getBanned] method.
        :param start_from: identifier required to get the next page of results. Value for this parameter is returned in 'next_from' field in a reply.
        :param count: Number of news items to return (default 50, maximum 100). For auto feed, you can use the 'new_offset' parameter returned by this method.
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        :param section: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.get", params)


class NewsfeedGetBanned(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, extended: bool, fields: typing.List, name_case: str):
        """ newsfeed.getBanned
        From Vk Docs: Returns a list of users and communities banned from the current user's newsfeed.
        Access from user token(s)
        :param extended: '1' — return extra information about users and communities
        :param fields: Profile fields to return.
        :param name_case: Case for declension of user name and surname: 'nom' — nominative (default), 'gen' — genitive , 'dat' — dative, 'acc' — accusative , 'ins' — instrumental , 'abl' — prepositional
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.getBanned", params)


class NewsfeedGetComments(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        count: int,
        filters: typing.List,
        reposts: str,
        start_time: int,
        end_time: int,
        last_comments_count: int,
        start_from: str,
        fields: typing.List,
    ):
        """ newsfeed.getComments
        From Vk Docs: Returns a list of comments in the current user's newsfeed.
        Access from user token(s)
        :param count: Number of comments to return. For auto feed, you can use the 'new_offset' parameter returned by this method.
        :param filters: Filters to apply: 'post' — new comments on wall posts, 'photo' — new comments on photos, 'video' — new comments on videos, 'topic' — new comments on discussions, 'note' — new comments on notes,
        :param reposts: Object ID, comments on repost of which shall be returned, e.g. 'wall1_45486'. (If the parameter is set, the 'filters' parameter is optional.),
        :param start_time: Earliest timestamp (in Unix time) of a comment to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a comment to return. By default, the current time.
        :param last_comments_count: 
        :param start_from: Identificator needed to return the next page with results. Value for this parameter returns in 'next_from' field.
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.getComments", params)


class NewsfeedGetLists(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, list_ids: typing.List, extended: bool):
        """ newsfeed.getLists
        From Vk Docs: Returns a list of newsfeeds followed by the current user.
        Access from user token(s)
        :param list_ids: numeric list identifiers.
        :param extended: Return additional list info
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.getLists", params)


class NewsfeedGetMentions(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, start_time: int, end_time: int, offset: int, count: int
    ):
        """ newsfeed.getMentions
        From Vk Docs: Returns a list of posts on user walls in which the current user is mentioned.
        Access from user token(s)
        :param owner_id: Owner ID.
        :param start_time: Earliest timestamp (in Unix time) of a post to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a post to return. By default, the current time.
        :param offset: Offset needed to return a specific subset of posts.
        :param count: Number of posts to return.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.getMentions", params)


class NewsfeedGetRecommended(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        start_time: int,
        end_time: int,
        max_photos: int,
        start_from: str,
        count: int,
        fields: typing.List,
    ):
        """ newsfeed.getRecommended
        From Vk Docs: , Returns a list of newsfeeds recommended to the current user.
        Access from user token(s)
        :param start_time: Earliest timestamp (in Unix time) of a news item to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a news item to return. By default, the current time.
        :param max_photos: Maximum number of photos to return. By default, '5'.
        :param start_from: 'new_from' value obtained in previous call.
        :param count: Number of news items to return.
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.getRecommended", params)


class NewsfeedGetSuggestedSources(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, offset: int, count: int, shuffle: bool, fields: typing.List
    ):
        """ newsfeed.getSuggestedSources
        From Vk Docs: Returns communities and users that current user is suggested to follow.
        Access from user token(s)
        :param offset: offset required to choose a particular subset of communities or users.
        :param count: amount of communities or users to return.
        :param shuffle: shuffle the returned list or not.
        :param fields: list of extra fields to be returned. See available fields for [vk.com/dev/fields|users] and [vk.com/dev/fields_groups|communities].
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.getSuggestedSources", params)


class NewsfeedIgnoreItem(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, type: str, owner_id: int, item_id: int):
        """ newsfeed.ignoreItem
        From Vk Docs: Hides an item from the newsfeed.
        Access from user token(s)
        :param type: Item type. Possible values: *'wall' – post on the wall,, *'tag' – tag on a photo,, *'profilephoto' – profile photo,, *'video' – video,, *'audio' – audio.
        :param owner_id: Item owner's identifier (user or community), "Note that community id must be negative. 'owner_id=1' – user , 'owner_id=-1' – community "
        :param item_id: Item identifier
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.ignoreItem", params)


class NewsfeedSaveList(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, list_id: int, title: str, source_ids: typing.List, no_reposts: bool
    ):
        """ newsfeed.saveList
        From Vk Docs: Creates and edits user newsfeed lists
        Access from user token(s)
        :param list_id: numeric list identifier (if not sent, will be set automatically).
        :param title: list name.
        :param source_ids: users and communities identifiers to be added to the list. Community identifiers must be negative numbers.
        :param no_reposts: reposts display on and off ('1' is for off).
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.saveList", params)


class NewsfeedSearch(BaseMethod):
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        q: str,
        extended: bool,
        count: int,
        latitude: typing.Any,
        longitude: typing.Any,
        start_time: int,
        end_time: int,
        start_from: str,
        fields: typing.List,
    ):
        """ newsfeed.search
        From Vk Docs: Returns search results by statuses.
        Access from user, service token(s)
        :param q: Search query string (e.g., 'New Year').
        :param extended: '1' — to return additional information about the user or community that placed the post.
        :param count: Number of posts to return.
        :param latitude: Geographical latitude point (in degrees, -90 to 90) within which to search.
        :param longitude: Geographical longitude point (in degrees, -180 to 180) within which to search.
        :param start_time: Earliest timestamp (in Unix time) of a news item to return. By default, 24 hours ago.
        :param end_time: Latest timestamp (in Unix time) of a news item to return. By default, the current time.
        :param start_from: 
        :param fields: Additional fields of [vk.com/dev/fields|profiles] and [vk.com/dev/fields_groups|communities] to return.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.search", params)


class NewsfeedUnignoreItem(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, type: str, owner_id: int, item_id: int):
        """ newsfeed.unignoreItem
        From Vk Docs: Returns a hidden item to the newsfeed.
        Access from user token(s)
        :param type: Item type. Possible values: *'wall' – post on the wall,, *'tag' – tag on a photo,, *'profilephoto' – profile photo,, *'video' – video,, *'audio' – audio.
        :param owner_id: Item owner's identifier (user or community), "Note that community id must be negative. 'owner_id=1' – user , 'owner_id=-1' – community "
        :param item_id: Item identifier
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.unignoreItem", params)


class NewsfeedUnsubscribe(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, type: str, owner_id: int, item_id: int):
        """ newsfeed.unsubscribe
        From Vk Docs: Unsubscribes the current user from specified newsfeeds.
        Access from user token(s)
        :param type: Type of object from which to unsubscribe: 'note' — note, 'photo' — photo, 'post' — post on user wall or community wall, 'topic' — topic, 'video' — video
        :param owner_id: Object owner ID.
        :param item_id: Object ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("newsfeed.unsubscribe", params)


class Newsfeed:
    def __init__(self, request):
        self.add_ban = NewsfeedAddBan(request)
        self.delete_ban = NewsfeedDeleteBan(request)
        self.delete_list = NewsfeedDeleteList(request)
        self.get = NewsfeedGet(request)
        self.get_banned = NewsfeedGetBanned(request)
        self.get_comments = NewsfeedGetComments(request)
        self.get_lists = NewsfeedGetLists(request)
        self.get_mentions = NewsfeedGetMentions(request)
        self.get_recommended = NewsfeedGetRecommended(request)
        self.get_suggested_sources = NewsfeedGetSuggestedSources(request)
        self.ignore_item = NewsfeedIgnoreItem(request)
        self.save_list = NewsfeedSaveList(request)
        self.search = NewsfeedSearch(request)
        self.unignore_item = NewsfeedUnignoreItem(request)
        self.unsubscribe = NewsfeedUnsubscribe(request)
