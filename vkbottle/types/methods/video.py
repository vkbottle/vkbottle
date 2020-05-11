# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class VideoAdd(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, video_id: int, target_id: int = None, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ video.add
        From Vk Docs: Adds a video to a user or community page.
        Access from user token(s)
        :param target_id: identifier of a user or community to add a video to. Use a negative value to designate a community ID.
        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video. Use a negative value to designate a community ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.add", params, response_model=responses.ok_response.OkResponseModel
        )


class VideoAddAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int = None, title: str = None, privacy: typing.List = None
    ) -> responses.video.AddAlbum:
        """ video.addAlbum
        From Vk Docs: Creates an empty album for videos.
        Access from user token(s)
        :param group_id: Community ID (if the album will be created in a community).
        :param title: Album title.
        :param privacy: new access permissions for the album. Possible values: , *'0' – all users,, *'1' – friends only,, *'2' – friends and friends of friends,, *'3' – "only me".
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.addAlbum", params, response_model=responses.video.AddAlbumModel
        )


class VideoAddToAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        target_id: int = None,
        album_id: int = None,
        album_ids: typing.List = None,
        video_id: int = None,
    ) -> responses.ok_response.OkResponse:
        """ video.addToAlbum
        From Vk Docs: 
        Access from user token(s)
        :param target_id: 
        :param album_id: 
        :param album_ids: 
        :param owner_id: 
        :param video_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.addToAlbum",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoCreateComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        video_id: int,
        owner_id: int = None,
        message: str = None,
        attachments: typing.List = None,
        from_group: bool = None,
        reply_to_comment: int = None,
        sticker_id: int = None,
        guid: str = None,
    ) -> responses.video.CreateComment:
        """ video.createComment
        From Vk Docs: Adds a new comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param message: New comment text.
        :param attachments: List of objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media attachment: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — ID of the media attachment owner. '<media_id>' — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        :param from_group: '1' — to post the comment from a community name (only if 'owner_id'<0)
        :param reply_to_comment: 
        :param sticker_id: 
        :param guid: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.createComment",
            params,
            response_model=responses.video.CreateCommentModel,
        )


class VideoDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, video_id: int, owner_id: int = None, target_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ video.delete
        From Vk Docs: Deletes a video from a user or community page.
        Access from user token(s)
        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video.
        :param target_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.delete", params, response_model=responses.ok_response.OkResponseModel
        )


class VideoDeleteAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, album_id: int, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ video.deleteAlbum
        From Vk Docs: Deletes a video album.
        Access from user token(s)
        :param group_id: Community ID (if the album is owned by a community).
        :param album_id: Album ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.deleteAlbum",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoDeleteComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, comment_id: int, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ video.deleteComment
        From Vk Docs: Deletes a comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the comment to be deleted.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.deleteComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        video_id: int,
        owner_id: int = None,
        name: str = None,
        desc: str = None,
        privacy_view: typing.List = None,
        privacy_comment: typing.List = None,
        no_comments: bool = None,
        repeat: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ video.edit
        From Vk Docs: Edits information about a video on a user or community page.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param name: New video title.
        :param desc: New video description.
        :param privacy_view: Privacy settings in a [vk.com/dev/privacy_setting|special format]. Privacy setting is available for videos uploaded to own profile by user.
        :param privacy_comment: Privacy settings for comments in a [vk.com/dev/privacy_setting|special format].
        :param no_comments: Disable comments for the group video.
        :param repeat: '1' — to repeat the playback of the video, '0' — to play the video once,
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.edit", params, response_model=responses.ok_response.OkResponseModel
        )


class VideoEditAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        album_id: int,
        group_id: int = None,
        title: str = None,
        privacy: typing.List = None,
    ) -> responses.ok_response.OkResponse:
        """ video.editAlbum
        From Vk Docs: Edits the title of a video album.
        Access from user token(s)
        :param group_id: Community ID (if the album edited is owned by a community).
        :param album_id: Album ID.
        :param title: New album title.
        :param privacy: new access permissions for the album. Possible values: , *'0' – all users,, *'1' – friends only,, *'2' – friends and friends of friends,, *'3' – "only me".
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.editAlbum",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoEditComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        comment_id: int,
        owner_id: int = None,
        message: str = None,
        attachments: typing.List = None,
    ) -> responses.ok_response.OkResponse:
        """ video.editComment
        From Vk Docs: Edits the text of a comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: Comment ID.
        :param message: New comment text.
        :param attachments: List of objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media attachment: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — ID of the media attachment owner. '<media_id>' — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.editComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoGet(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int = None,
        videos: typing.List = None,
        album_id: int = None,
        count: int = None,
        offset: int = None,
        extended: bool = None,
    ) -> responses.video.Get:
        """ video.get
        From Vk Docs: Returns detailed information about videos.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video(s).
        :param videos: Video IDs, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", Use a negative value to designate a community ID. Example: "-4363_136089719,13245770_137352259"
        :param album_id: ID of the album containing the video(s).
        :param count: Number of videos to return.
        :param offset: Offset needed to return a specific subset of videos.
        :param extended: '1' — to return an extended response with additional fields
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.get", params, response_model=responses.video.GetModel
        )


class VideoGetAlbumById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, album_id: int, owner_id: int = None
    ) -> responses.video.GetAlbumById:
        """ video.getAlbumById
        From Vk Docs: Returns video album info
        Access from user token(s)
        :param owner_id: identifier of a user or community to add a video to. Use a negative value to designate a community ID.
        :param album_id: Album ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.getAlbumById",
            params,
            response_model=responses.video.GetAlbumByIdModel,
        )


class VideoGetAlbums(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int = None,
        offset: int = None,
        count: int = None,
        extended: bool = None,
        need_system: bool = None,
    ) -> responses.video.GetAlbums:
        """ video.getAlbums
        From Vk Docs: Returns a list of video albums owned by a user or community.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video album(s).
        :param offset: Offset needed to return a specific subset of video albums.
        :param count: Number of video albums to return.
        :param extended: '1' — to return additional information about album privacy settings for the current user
        :param need_system: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.getAlbums", params, response_model=responses.video.GetAlbumsModel
        )


class VideoGetAlbumsByVideo(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        target_id: int = None,
        video_id: int = None,
        extended: bool = None,
    ) -> responses.video.GetAlbumsByVideo:
        """ video.getAlbumsByVideo
        From Vk Docs: 
        Access from user token(s)
        :param target_id: 
        :param owner_id: 
        :param video_id: 
        :param extended: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.getAlbumsByVideo",
            params,
            response_model=responses.video.GetAlbumsByVideoModel,
        )


class VideoGetComments(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        video_id: int,
        owner_id: int = None,
        need_likes: bool = None,
        start_comment_id: int = None,
        offset: int = None,
        count: int = None,
        sort: str = None,
        extended: bool = None,
        fields: typing.List = None,
    ) -> responses.video.GetComments:
        """ video.getComments
        From Vk Docs: Returns a list of comments on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param need_likes: '1' — to return an additional 'likes' field
        :param start_comment_id: 
        :param offset: Offset needed to return a specific subset of comments.
        :param count: Number of comments to return.
        :param sort: Sort order: 'asc' — oldest comment first, 'desc' — newest comment first
        :param extended: 
        :param fields: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.getComments", params, response_model=responses.video.GetCommentsModel
        )


class VideoRemoveFromAlbum(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        target_id: int = None,
        album_id: int = None,
        album_ids: typing.List = None,
        video_id: int = None,
    ) -> responses.ok_response.OkResponse:
        """ video.removeFromAlbum
        From Vk Docs: 
        Access from user token(s)
        :param target_id: 
        :param album_id: 
        :param album_ids: 
        :param owner_id: 
        :param video_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.removeFromAlbum",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoReorderAlbums(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, album_id: int, owner_id: int = None, before: int = None, after: int = None
    ) -> responses.ok_response.OkResponse:
        """ video.reorderAlbums
        From Vk Docs: Reorders the album in the list of user video albums.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the albums..
        :param album_id: Album ID.
        :param before: ID of the album before which the album in question shall be placed.
        :param after: ID of the album after which the album in question shall be placed.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.reorderAlbums",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoReorderVideos(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        target_id: int = None,
        album_id: int = None,
        video_id: int = None,
        before_owner_id: int = None,
        before_video_id: int = None,
        after_owner_id: int = None,
        after_video_id: int = None,
    ) -> responses.ok_response.OkResponse:
        """ video.reorderVideos
        From Vk Docs: Reorders the video in the video album.
        Access from user token(s)
        :param target_id: ID of the user or community that owns the album with videos.
        :param album_id: ID of the video album.
        :param owner_id: ID of the user or community that owns the video.
        :param video_id: ID of the video.
        :param before_owner_id: ID of the user or community that owns the video before which the video in question shall be placed.
        :param before_video_id: ID of the video before which the video in question shall be placed.
        :param after_owner_id: ID of the user or community that owns the video after which the photo in question shall be placed.
        :param after_video_id: ID of the video after which the photo in question shall be placed.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.reorderVideos",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoReport(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        video_id: int,
        reason: int = None,
        comment: str = None,
        search_query: str = None,
    ) -> responses.ok_response.OkResponse:
        """ video.report
        From Vk Docs: Reports (submits a complaint about) a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param reason: Reason for the complaint: '0' – spam, '1' – child pornography, '2' – extremism, '3' – violence, '4' – drug propaganda, '5' – adult material, '6' – insult, abuse
        :param comment: Comment describing the complaint.
        :param search_query: (If the video was found in search results.) Search query string.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.report", params, response_model=responses.ok_response.OkResponseModel
        )


class VideoReportComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, comment_id: int, reason: int = None
    ) -> responses.ok_response.OkResponse:
        """ video.reportComment
        From Vk Docs: Reports (submits a complaint about) a comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the comment being reported.
        :param reason: Reason for the complaint: , 0 – spam , 1 – child pornography , 2 – extremism , 3 – violence , 4 – drug propaganda , 5 – adult material , 6 – insult, abuse
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.reportComment",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoRestore(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, video_id: int, owner_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ video.restore
        From Vk Docs: Restores a previously deleted video.
        Access from user token(s)
        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.restore",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class VideoRestoreComment(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, comment_id: int, owner_id: int = None
    ) -> responses.video.RestoreComment:
        """ video.restoreComment
        From Vk Docs: Restores a previously deleted comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the deleted comment.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.restoreComment",
            params,
            response_model=responses.video.RestoreCommentModel,
        )


class VideoSave(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        name: str = None,
        description: str = None,
        is_private: bool = None,
        wallpost: bool = None,
        link: str = None,
        group_id: int = None,
        album_id: int = None,
        privacy_view: typing.List = None,
        privacy_comment: typing.List = None,
        no_comments: bool = None,
        repeat: bool = None,
        compression: bool = None,
    ) -> responses.video.Save:
        """ video.save
        From Vk Docs: Returns a server address (required for upload) and video data.
        Access from user token(s)
        :param name: Name of the video.
        :param description: Description of the video.
        :param is_private: '1' — to designate the video as private (send it via a private message), the video will not appear on the user's video list and will not be available by ID for other users, '0' — not to designate the video as private
        :param wallpost: '1' — to post the saved video on a user's wall, '0' — not to post the saved video on a user's wall
        :param link: URL for embedding the video from an external website.
        :param group_id: ID of the community in which the video will be saved. By default, the current user's page.
        :param album_id: ID of the album to which the saved video will be added.
        :param privacy_view: 
        :param privacy_comment: 
        :param no_comments: 
        :param repeat: '1' — to repeat the playback of the video, '0' — to play the video once,
        :param compression: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.save", params, response_model=responses.video.SaveModel
        )


class VideoSearch(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        q: str,
        sort: int = None,
        hd: int = None,
        adult: bool = None,
        filters: typing.List = None,
        search_own: bool = None,
        offset: int = None,
        longer: int = None,
        shorter: int = None,
        count: int = None,
        extended: bool = None,
    ) -> responses.video.Search:
        """ video.search
        From Vk Docs: Returns a list of videos under the set search criterion.
        Access from user token(s)
        :param q: Search query string (e.g., 'The Beatles').
        :param sort: Sort order: '1' — by duration, '2' — by relevance, '0' — by date added
        :param hd: If not null, only searches for high-definition videos.
        :param adult: '1' — to disable the Safe Search filter, '0' — to enable the Safe Search filter
        :param filters: Filters to apply: 'youtube' — return YouTube videos only, 'vimeo' — return Vimeo videos only, 'short' — return short videos only, 'long' — return long videos only
        :param search_own: 
        :param offset: Offset needed to return a specific subset of videos.
        :param longer: 
        :param shorter: 
        :param count: Number of videos to return.
        :param extended: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "video.search", params, response_model=responses.video.SearchModel
        )


class Video:
    def __init__(self, request):
        self.add = VideoAdd(request)
        self.add_album = VideoAddAlbum(request)
        self.add_to_album = VideoAddToAlbum(request)
        self.create_comment = VideoCreateComment(request)
        self.delete = VideoDelete(request)
        self.delete_album = VideoDeleteAlbum(request)
        self.delete_comment = VideoDeleteComment(request)
        self.edit = VideoEdit(request)
        self.edit_album = VideoEditAlbum(request)
        self.edit_comment = VideoEditComment(request)
        self.get = VideoGet(request)
        self.get_album_by_id = VideoGetAlbumById(request)
        self.get_albums = VideoGetAlbums(request)
        self.get_albums_by_video = VideoGetAlbumsByVideo(request)
        self.get_comments = VideoGetComments(request)
        self.remove_from_album = VideoRemoveFromAlbum(request)
        self.reorder_albums = VideoReorderAlbums(request)
        self.reorder_videos = VideoReorderVideos(request)
        self.report = VideoReport(request)
        self.report_comment = VideoReportComment(request)
        self.restore = VideoRestore(request)
        self.restore_comment = VideoRestoreComment(request)
        self.save = VideoSave(request)
        self.search = VideoSearch(request)
