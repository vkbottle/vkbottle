# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class BoardAddTopic(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        title: str,
        text: str = None,
        from_group: bool = None,
        attachments: typing.List = None,
    ) -> responses.board.AddTopic:
        """ board.addTopic
        From Vk Docs: Creates a new topic on a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param title: Topic title.
        :param text: Text of the topic.
        :param from_group: For a community: '1' — to post the topic as by the community, '0' — to post the topic as by the user (default)
        :param attachments: List of media objects attached to the topic, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media object: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — ID of the media owner. '<media_id>' — Media ID. Example: "photo100172_166443618,photo66748_265827614", , "NOTE: If you try to attach more than one reference, an error will be thrown.",
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.addTopic", params, response_model=responses.board.AddTopicModel
        )


class BoardCloseTopic(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.closeTopic
        From Vk Docs: Closes a topic on a community's discussion board so that comments cannot be posted.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.closeTopic",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardCreateComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        topic_id: int,
        message: str = None,
        attachments: typing.List = None,
        from_group: bool = None,
        sticker_id: int = None,
        guid: str = None,
    ) -> responses.board.CreateComment:
        """ board.createComment
        From Vk Docs: Adds a comment on a topic on a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: ID of the topic to be commented on.
        :param message: (Required if 'attachments' is not set.) Text of the comment.
        :param attachments: (Required if 'text' is not set.) List of media objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media object: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — ID of the media owner. '<media_id>' — Media ID.
        :param from_group: '1' — to post the comment as by the community, '0' — to post the comment as by the user (default)
        :param sticker_id: Sticker ID.
        :param guid: Unique identifier to avoid repeated comments.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.createComment",
            params,
            response_model=responses.board.CreateCommentModel,
        )


class BoardDeleteComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int, comment_id: int, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.deleteComment
        From Vk Docs: Deletes a comment on a topic on a community's discussion board.
        Access from user, group token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param comment_id: Comment ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.deleteComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardDeleteTopic(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.deleteTopic
        From Vk Docs: Deletes a topic from a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.deleteTopic",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardEditComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        group_id: int,
        comment_id: int,
        topic_id: int,
        message: str = None,
        attachments: typing.List = None,
    ) -> responses.ok_response.OkResponse:
        """ board.editComment
        From Vk Docs: Edits a comment on a topic on a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param comment_id: ID of the comment on the topic.
        :param message: (Required if 'attachments' is not set). New comment text.
        :param attachments: (Required if 'message' is not set.) List of media objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media object: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — ID of the media owner. '<media_id>' — Media ID. Example: "photo100172_166443618,photo66748_265827614"
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.editComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardEditTopic(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, title: str, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.editTopic
        From Vk Docs: Edits the title of a topic on a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param title: New title of the topic.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.editTopic",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardFixTopic(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.fixTopic
        From Vk Docs: Pins a topic (fixes its place) to the top of a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.fixTopic",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardGetComments(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        group_id: int,
        topic_id: int,
        need_likes: bool = None,
        start_comment_id: int = None,
        offset: int = None,
        count: int = None,
        extended: bool = None,
        sort: str = None,
    ) -> responses.board.GetComments:
        """ board.getComments
        From Vk Docs: Returns a list of comments on a topic on a community's discussion board.
        Access from user, service token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param need_likes: '1' — to return the 'likes' field, '0' — not to return the 'likes' field (default)
        :param start_comment_id: 
        :param offset: Offset needed to return a specific subset of comments.
        :param count: Number of comments to return.
        :param extended: '1' — to return information about users who posted comments, '0' — to return no additional fields (default)
        :param sort: Sort order: 'asc' — by creation date in chronological order, 'desc' — by creation date in reverse chronological order,
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.getComments", params, response_model=responses.board.GetCommentsModel
        )


class BoardGetTopics(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.SERVICE,
    ]

    async def __call__(
        self,
        group_id: int,
        topic_ids: typing.List = None,
        order: int = None,
        offset: int = None,
        count: int = None,
        extended: bool = None,
        preview: int = None,
        preview_length: int = None,
    ) -> responses.board.GetTopics:
        """ board.getTopics
        From Vk Docs: Returns a list of topics on a community's discussion board.
        Access from user, service token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_ids: IDs of topics to be returned (100 maximum). By default, all topics are returned. If this parameter is set, the 'order', 'offset', and 'count' parameters are ignored.
        :param order: Sort order: '1' — by date updated in reverse chronological order. '2' — by date created in reverse chronological order. '-1' — by date updated in chronological order. '-2' — by date created in chronological order. If no sort order is specified, topics are returned in the order specified by the group administrator. Pinned topics are returned first, regardless of the sorting.
        :param offset: Offset needed to return a specific subset of topics.
        :param count: Number of topics to return.
        :param extended: '1' — to return information about users who created topics or who posted there last, '0' — to return no additional fields (default)
        :param preview: '1' — to return the first comment in each topic,, '2' — to return the last comment in each topic,, '0' — to return no comments. By default: '0'.
        :param preview_length: Number of characters after which to truncate the previewed comment. To preview the full comment, specify '0'.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.getTopics", params, response_model=responses.board.GetTopicsModel
        )


class BoardOpenTopic(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.openTopic
        From Vk Docs: Re-opens a previously closed topic on a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.openTopic",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardRestoreComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int, comment_id: int, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.restoreComment
        From Vk Docs: Restores a comment deleted from a topic on a community's discussion board.
        Access from user, group token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        :param comment_id: Comment ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.restoreComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class BoardUnfixTopic(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, topic_id: int
    ) -> responses.ok_response.OkResponse:
        """ board.unfixTopic
        From Vk Docs: Unpins a pinned topic from the top of a community's discussion board.
        Access from user token(s)
        :param group_id: ID of the community that owns the discussion board.
        :param topic_id: Topic ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "board.unfixTopic",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class Board:
    def __init__(self, request):
        self.add_topic = BoardAddTopic(request)
        self.close_topic = BoardCloseTopic(request)
        self.create_comment = BoardCreateComment(request)
        self.delete_comment = BoardDeleteComment(request)
        self.delete_topic = BoardDeleteTopic(request)
        self.edit_comment = BoardEditComment(request)
        self.edit_topic = BoardEditTopic(request)
        self.fix_topic = BoardFixTopic(request)
        self.get_comments = BoardGetComments(request)
        self.get_topics = BoardGetTopics(request)
        self.open_topic = BoardOpenTopic(request)
        self.restore_comment = BoardRestoreComment(request)
        self.unfix_topic = BoardUnfixTopic(request)
