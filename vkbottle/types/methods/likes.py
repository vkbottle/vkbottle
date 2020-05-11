# Generated with love
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class LikesAdd(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, type: str, item_id: int, owner_id: int = None, access_key: str = None
    ) -> responses.likes.Add:
        """ likes.add
        From Vk Docs: Adds the specified object to the 'Likes' list of the current user.
        Access from user token(s)
        :param type: Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion, 'sitepage' — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.
        :param access_key: Access key required for an object owned by a private entity.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "likes.add", params, response_model=responses.likes.AddModel
        )


class LikesDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, type: str, item_id: int, owner_id: int = None
    ) -> responses.likes.Delete:
        """ likes.delete
        From Vk Docs: Deletes the specified object from the 'Likes' list of the current user.
        Access from user token(s)
        :param type: Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion, 'sitepage' — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "likes.delete", params, response_model=responses.likes.DeleteModel
        )


class LikesGetList(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        type: str,
        owner_id: int = None,
        item_id: int = None,
        page_url: str = None,
        filter: str = None,
        friends_only: int = None,
        extended: bool = None,
        offset: int = None,
        count: int = None,
        skip_own: bool = None,
    ) -> responses.likes.GetList:
        """ likes.getList
        From Vk Docs: Returns a list of IDs of users who added the specified object to their 'Likes' list.
        Access from user, service token(s)
        :param type: , Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion, 'sitepage' — page of the site where the [vk.com/dev/Like|Like widget] is installed
        :param owner_id: ID of the user, community, or application that owns the object. If the 'type' parameter is set as 'sitepage', the application ID is passed as 'owner_id'. Use negative value for a community id. If the 'type' parameter is not set, the 'owner_id' is assumed to be either the current user or the same application ID as if the 'type' parameter was set to 'sitepage'.
        :param item_id: Object ID. If 'type' is set as 'sitepage', 'item_id' can include the 'page_id' parameter value used during initialization of the [vk.com/dev/Like|Like widget].
        :param page_url: URL of the page where the [vk.com/dev/Like|Like widget] is installed. Used instead of the 'item_id' parameter.
        :param filter: Filters to apply: 'likes' — returns information about all users who liked the object (default), 'copies' — returns information only about users who told their friends about the object
        :param friends_only: Specifies which users are returned: '1' — to return only the current user's friends, '0' — to return all users (default)
        :param extended: Specifies whether extended information will be returned. '1' — to return extended information about users and communities from the 'Likes' list, '0' — to return no additional information (default)
        :param offset: Offset needed to select a specific subset of users.
        :param count: Number of user IDs to return (maximum '1000'). Default is '100' if 'friends_only' is set to '0', otherwise, the default is '10' if 'friends_only' is set to '1'.
        :param skip_own: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "likes.getList", params, response_model=responses.likes.GetListModel
        )


class LikesIsLiked(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, type: str, item_id: int, user_id: int = None, owner_id: int = None
    ) -> responses.likes.IsLiked:
        """ likes.isLiked
        From Vk Docs: Checks for the object in the 'Likes' list of the specified user.
        Access from user token(s)
        :param user_id: User ID.
        :param type: Object type: 'post' — post on user or community wall, 'comment' — comment on a wall post, 'photo' — photo, 'audio' — audio, 'video' — video, 'note' — note, 'photo_comment' — comment on the photo, 'video_comment' — comment on the video, 'topic_comment' — comment in the discussion
        :param owner_id: ID of the user or community that owns the object.
        :param item_id: Object ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "likes.isLiked", params, response_model=responses.likes.IsLikedModel
        )


class Likes:
    def __init__(self, request):
        self.add = LikesAdd(request)
        self.delete = LikesDelete(request)
        self.get_list = LikesGetList(request)
        self.is_liked = LikesIsLiked(request)
