# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class VideoAdd(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, target_id: int, video_id: int, owner_id: int):
        """ video.add
        From Vk Docs: Adds a video to a user or community page.
        Access from user token(s)
        :param target_id: identifier of a user or community to add a video to. Use a negative value to designate a community ID.
        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video. Use a negative value to designate a community ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.add", params)


class VideoAddAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int, title: str, privacy: typing.List):
        """ video.addAlbum
        From Vk Docs: Creates an empty album for videos.
        Access from user token(s)
        :param group_id: Community ID (if the album will be created in a community).
        :param title: Album title.
        :param privacy: new access permissions for the album. Possible values: , *'0' – all users,, *'1' – friends only,, *'2' – friends and friends of friends,, *'3' – "only me".
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.addAlbum", params)


class VideoAddToAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        target_id: int,
        album_id: int,
        album_ids: typing.List,
        owner_id: int,
        video_id: int,
    ):
        """ video.addToAlbum
        From Vk Docs: 
        Access from user token(s)
        :param target_id: 
        :param album_id: 
        :param album_ids: 
        :param owner_id: 
        :param video_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.addToAlbum", params)


class VideoCreateComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        video_id: int,
        message: str,
        attachments: typing.List,
        from_group: bool,
        reply_to_comment: int,
        sticker_id: int,
        guid: str,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.createComment", params)


class VideoDelete(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, video_id: int, owner_id: int, target_id: int):
        """ video.delete
        From Vk Docs: Deletes a video from a user or community page.
        Access from user token(s)
        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video.
        :param target_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.delete", params)


class VideoDeleteAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int, album_id: int):
        """ video.deleteAlbum
        From Vk Docs: Deletes a video album.
        Access from user token(s)
        :param group_id: Community ID (if the album is owned by a community).
        :param album_id: Album ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.deleteAlbum", params)


class VideoDeleteComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, comment_id: int):
        """ video.deleteComment
        From Vk Docs: Deletes a comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the comment to be deleted.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.deleteComment", params)


class VideoEdit(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        video_id: int,
        name: str,
        desc: str,
        privacy_view: typing.List,
        privacy_comment: typing.List,
        no_comments: bool,
        repeat: bool,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.edit", params)


class VideoEditAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, album_id: int, title: str, privacy: typing.List
    ):
        """ video.editAlbum
        From Vk Docs: Edits the title of a video album.
        Access from user token(s)
        :param group_id: Community ID (if the album edited is owned by a community).
        :param album_id: Album ID.
        :param title: New album title.
        :param privacy: new access permissions for the album. Possible values: , *'0' – all users,, *'1' – friends only,, *'2' – friends and friends of friends,, *'3' – "only me".
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.editAlbum", params)


class VideoEditComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, comment_id: int, message: str, attachments: typing.List
    ):
        """ video.editComment
        From Vk Docs: Edits the text of a comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: Comment ID.
        :param message: New comment text.
        :param attachments: List of objects attached to the comment, in the following format: "<owner_id>_<media_id>,<owner_id>_<media_id>", '' — Type of media attachment: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, '<owner_id>' — ID of the media attachment owner. '<media_id>' — Media attachment ID. Example: "photo100172_166443618,photo66748_265827614"
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.editComment", params)


class VideoGet(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        videos: typing.List,
        album_id: int,
        count: int,
        offset: int,
        extended: bool,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.get", params)


class VideoGetAlbumById(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, album_id: int):
        """ video.getAlbumById
        From Vk Docs: Returns video album info
        Access from user token(s)
        :param owner_id: identifier of a user or community to add a video to. Use a negative value to designate a community ID.
        :param album_id: Album ID.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.getAlbumById", params)


class VideoGetAlbums(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, offset: int, count: int, extended: bool, need_system: bool
    ):
        """ video.getAlbums
        From Vk Docs: Returns a list of video albums owned by a user or community.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video album(s).
        :param offset: Offset needed to return a specific subset of video albums.
        :param count: Number of video albums to return.
        :param extended: '1' — to return additional information about album privacy settings for the current user
        :param need_system: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.getAlbums", params)


class VideoGetAlbumsByVideo(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, target_id: int, owner_id: int, video_id: int, extended: bool
    ):
        """ video.getAlbumsByVideo
        From Vk Docs: 
        Access from user token(s)
        :param target_id: 
        :param owner_id: 
        :param video_id: 
        :param extended: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.getAlbumsByVideo", params)


class VideoGetComments(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        video_id: int,
        need_likes: bool,
        start_comment_id: int,
        offset: int,
        count: int,
        sort: str,
        extended: bool,
        fields: typing.List,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.getComments", params)


class VideoRemoveFromAlbum(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        target_id: int,
        album_id: int,
        album_ids: typing.List,
        owner_id: int,
        video_id: int,
    ):
        """ video.removeFromAlbum
        From Vk Docs: 
        Access from user token(s)
        :param target_id: 
        :param album_id: 
        :param album_ids: 
        :param owner_id: 
        :param video_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.removeFromAlbum", params)


class VideoReorderAlbums(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, album_id: int, before: int, after: int):
        """ video.reorderAlbums
        From Vk Docs: Reorders the album in the list of user video albums.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the albums..
        :param album_id: Album ID.
        :param before: ID of the album before which the album in question shall be placed.
        :param after: ID of the album after which the album in question shall be placed.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.reorderAlbums", params)


class VideoReorderVideos(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        target_id: int,
        album_id: int,
        owner_id: int,
        video_id: int,
        before_owner_id: int,
        before_video_id: int,
        after_owner_id: int,
        after_video_id: int,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.reorderVideos", params)


class VideoReport(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, video_id: int, reason: int, comment: str, search_query: str
    ):
        """ video.report
        From Vk Docs: Reports (submits a complaint about) a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param video_id: Video ID.
        :param reason: Reason for the complaint: '0' – spam, '1' – child pornography, '2' – extremism, '3' – violence, '4' – drug propaganda, '5' – adult material, '6' – insult, abuse
        :param comment: Comment describing the complaint.
        :param search_query: (If the video was found in search results.) Search query string.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.report", params)


class VideoReportComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, comment_id: int, reason: int):
        """ video.reportComment
        From Vk Docs: Reports (submits a complaint about) a comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the comment being reported.
        :param reason: Reason for the complaint: , 0 – spam , 1 – child pornography , 2 – extremism , 3 – violence , 4 – drug propaganda , 5 – adult material , 6 – insult, abuse
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.reportComment", params)


class VideoRestore(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, video_id: int, owner_id: int):
        """ video.restore
        From Vk Docs: Restores a previously deleted video.
        Access from user token(s)
        :param video_id: Video ID.
        :param owner_id: ID of the user or community that owns the video.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.restore", params)


class VideoRestoreComment(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, owner_id: int, comment_id: int):
        """ video.restoreComment
        From Vk Docs: Restores a previously deleted comment on a video.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the video.
        :param comment_id: ID of the deleted comment.
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.restoreComment", params)


class VideoSave(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        name: str,
        description: str,
        is_private: bool,
        wallpost: bool,
        link: str,
        group_id: int,
        album_id: int,
        privacy_view: typing.List,
        privacy_comment: typing.List,
        no_comments: bool,
        repeat: bool,
        compression: bool,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.save", params)


class VideoSearch(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        q: str,
        sort: int,
        hd: int,
        adult: bool,
        filters: typing.List,
        search_own: bool,
        offset: int,
        longer: int,
        shorter: int,
        count: int,
        extended: bool,
    ):
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

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("video.search", params)


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
