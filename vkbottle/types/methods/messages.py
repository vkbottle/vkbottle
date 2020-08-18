# Generated with love
import typing
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class MessagesAddChatUser(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, chat_id: int, user_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ messages.addChatUser
        From Vk Docs: Adds a new user to a chat.
        Access from user token(s)
        :param chat_id: Chat ID.
        :param user_id: ID of the user to be added to the chat.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.addChatUser",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesAllowMessagesFromGroup(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, group_id: int, key: str = None
    ) -> responses.ok_response.OkResponse:
        """ messages.allowMessagesFromGroup
        From Vk Docs: Allows sending messages from community to the current user.
        Access from user token(s)
        :param group_id: Group ID.
        :param key: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.allowMessagesFromGroup",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesCreateChat(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, user_ids: typing.List = None, title: str = None,
    ) -> responses.messages.CreateChat:
        """ messages.createChat
        From Vk Docs: Creates a chat with several participants.
        Access from user token(s)
        :param user_ids: IDs of the users to be added to the chat.
        :param title: Chat title.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.createChat",
            params,
            response_model=responses.messages.CreateChatModel,
        )


class MessagesDelete(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        message_ids: typing.List = None,
        spam: bool = None,
        group_id: int = None,
        delete_for_all: bool = None,
    ) -> responses.ok_response.OkResponse:
        """ messages.delete
        From Vk Docs: Deletes one or more messages.
        Access from user, group token(s)
        :param message_ids: Message IDs.
        :param spam: '1' — to mark message as spam.
        :param group_id: Group ID (for group messages with user access token)
        :param delete_for_all: '1' — delete message for for all.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.delete",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesDeleteChatPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, chat_id: int, group_id: int = None
    ) -> responses.messages.DeleteChatPhoto:
        """ messages.deleteChatPhoto
        From Vk Docs: Deletes a chat's cover picture.
        Access from user, group token(s)
        :param chat_id: Chat ID.
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.deleteChatPhoto",
            params,
            response_model=responses.messages.DeleteChatPhotoModel,
        )


class MessagesDeleteConversation(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, user_id: int = None, peer_id: int = None, group_id: int = None
    ) -> responses.messages.DeleteConversation:
        """ messages.deleteConversation
        From Vk Docs: Deletes all private messages in a conversation.
        Access from user, group token(s)
        :param user_id: User ID. To clear a chat history use 'chat_id'
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param group_id: Group ID (for group messages with user access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.deleteConversation",
            params,
            response_model=responses.messages.DeleteConversationModel,
        )


class MessagesDenyMessagesFromGroup(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, group_id: int) -> responses.ok_response.OkResponse:
        """ messages.denyMessagesFromGroup
        From Vk Docs: Denies sending message from community to the current user.
        Access from user token(s)
        :param group_id: Group ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.denyMessagesFromGroup",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesEdit(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        peer_id: int,
        message_id: int,
        message: str = None,
        lat: typing.Any = None,
        long: typing.Any = None,
        attachment: str = None,
        keep_forward_messages: bool = None,
        keep_snippets: bool = None,
        group_id: int = None,
        dont_parse_links: bool = None,
    ) -> responses.messages.Edit:
        """ messages.edit
        From Vk Docs: Edits the message.
        Access from user, group token(s)
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param message: (Required if 'attachments' is not set.) Text of the message.
        :param message_id: 
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param attachment: (Required if 'message' is not set.) List of objects attached to the message, separated by commas, in the following format: "<owner_id>_<media_id>", '' — Type of media attachment: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, 'wall' — wall post, '<owner_id>' — ID of the media attachment owner. '<media_id>' — media attachment ID. Example: "photo100172_166443618"
        :param keep_forward_messages: '1' — to keep forwarded, messages.
        :param keep_snippets: '1' — to keep attached snippets.
        :param group_id: Group ID (for group messages with user access token)
        :param dont_parse_links: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.edit", params, response_model=responses.messages.EditModel
        )


class MessagesEditChat(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, chat_id: int, title: str
    ) -> responses.ok_response.OkResponse:
        """ messages.editChat
        From Vk Docs: Edits the title of a chat.
        Access from user, group token(s)
        :param chat_id: Chat ID.
        :param title: New title of the chat.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.editChat",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesGetByConversationMessageId(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        peer_id: int,
        conversation_message_ids: typing.List,
        extended: bool = None,
        fields: typing.List = None,
        group_id: int = None,
    ) -> responses.messages.GetByConversationMessageId:
        """ messages.getByConversationMessageId
        From Vk Docs: Returns messages by their IDs within the conversation.
        Access from user, group token(s)
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param conversation_message_ids: Conversation message IDs.
        :param extended: Information whether the response should be extended
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getByConversationMessageId",
            params,
            response_model=responses.messages.GetByConversationMessageIdModel,
        )


class MessagesGetById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        message_ids: typing.List,
        preview_length: int = None,
        extended: bool = None,
        fields: typing.List = None,
        group_id: int = None,
    ) -> responses.messages.GetById:
        """ messages.getById
        From Vk Docs: Returns messages by their IDs.
        Access from user, group token(s)
        :param message_ids: Message IDs.
        :param preview_length: Number of characters after which to truncate a previewed message. To preview the full message, specify '0'. "NOTE: Messages are not truncated by default. Messages are truncated by words."
        :param extended: Information whether the response should be extended
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getById", params, response_model=responses.messages.GetByIdModel
        )


class MessagesGetChatPreview(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, peer_id: int = None, link: str = None, fields: typing.List = None
    ) -> responses.messages.GetChatPreview:
        """ messages.getChatPreview
        From Vk Docs: 
        Access from user token(s)
        :param peer_id: 
        :param link: Invitation link.
        :param fields: Profile fields to return.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getChatPreview",
            params,
            response_model=responses.messages.GetChatPreviewModel,
        )


class MessagesGetConversationMembers(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, peer_id: int, fields: typing.List = None, group_id: int = None
    ) -> responses.messages.GetConversationMembers:
        """ messages.getConversationMembers
        From Vk Docs: Returns a list of IDs of users participating in a chat.
        Access from user, group token(s)
        :param peer_id: Peer ID.
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getConversationMembers",
            params,
            response_model=responses.messages.GetConversationMembersModel,
        )


class MessagesGetConversations(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        offset: int = None,
        count: int = None,
        filter: str = None,
        extended: bool = None,
        start_message_id: int = None,
        fields: typing.List = None,
        group_id: int = None,
    ) -> responses.messages.GetConversations:
        """ messages.getConversations
        From Vk Docs: Returns a list of the current user's conversations.
        Access from user, group token(s)
        :param offset: Offset needed to return a specific subset of conversations.
        :param count: Number of conversations to return.
        :param filter: Filter to apply: 'all' — all conversations, 'unread' — conversations with unread messages, 'important' — conversations, marked as important (only for community messages), 'unanswered' — conversations, marked as unanswered (only for community messages)
        :param extended: '1' — return extra information about users and communities
        :param start_message_id: ID of the message from what to return dialogs.
        :param fields: Profile and communities fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getConversations",
            params,
            response_model=responses.messages.GetConversationsModel,
        )


class MessagesGetConversationsById(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        peer_ids: typing.List,
        extended: bool = None,
        fields: typing.List = None,
        group_id: int = None,
    ) -> responses.messages.GetConversationsById:
        """ messages.getConversationsById
        From Vk Docs: Returns conversations by their IDs
        Access from user, group token(s)
        :param peer_ids: Destination IDs. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param extended: Return extended properties
        :param fields: Profile and communities fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getConversationsById",
            params,
            response_model=responses.messages.GetConversationsByIdModel,
        )


class MessagesGetHistory(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        offset: int = None,
        count: int = None,
        user_id: int = None,
        peer_id: int = None,
        start_message_id: int = None,
        rev: int = None,
        extended: bool = None,
        fields: typing.List = None,
        group_id: int = None,
    ) -> responses.messages.GetHistory:
        """ messages.getHistory
        From Vk Docs: Returns message history for the specified user or group chat.
        Access from user, group token(s)
        :param offset: Offset needed to return a specific subset of messages.
        :param count: Number of messages to return.
        :param user_id: ID of the user whose message history you want to return.
        :param peer_id: 
        :param start_message_id: Starting message ID from which to return history.
        :param rev: Sort order: '1' — return messages in chronological order. '0' — return messages in reverse chronological order.
        :param extended: Information whether the response should be extended
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getHistory",
            params,
            response_model=responses.messages.GetHistoryModel,
        )


class MessagesGetHistoryAttachments(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        peer_id: int,
        media_type: str = None,
        start_from: str = None,
        count: int = None,
        photo_sizes: bool = None,
        fields: typing.List = None,
        group_id: int = None,
        preserve_order: bool = None,
        max_forwards_level: int = None,
    ) -> responses.messages.GetHistoryAttachments:
        """ messages.getHistoryAttachments
        From Vk Docs: Returns media files from the dialog or group chat.
        Access from user, group token(s)
        :param peer_id: Peer ID. ", For group chat: '2000000000 + chat ID' , , For community: '-community ID'"
        :param media_type: Type of media files to return: *'photo',, *'video',, *'audio',, *'doc',, *'link'.,*'market'.,*'wall'.,*'share'
        :param start_from: Message ID to start return results from.
        :param count: Number of objects to return.
        :param photo_sizes: '1' — to return photo sizes in a
        :param fields: Additional profile [vk.com/dev/fields|fields] to return. 
        :param group_id: Group ID (for group messages with group access token)
        :param preserve_order: 
        :param max_forwards_level: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getHistoryAttachments",
            params,
            response_model=responses.messages.GetHistoryAttachmentsModel,
        )


class MessagesGetInviteLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, peer_id: int, reset: bool = None, group_id: int = None
    ) -> responses.messages.GetInviteLink:
        """ messages.getInviteLink
        From Vk Docs: 
        Access from user, group token(s)
        :param peer_id: Destination ID.
        :param reset: 1 — to generate new link (revoke previous), 0 — to return previous link.
        :param group_id: Group ID
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getInviteLink",
            params,
            response_model=responses.messages.GetInviteLinkModel,
        )


class MessagesGetLastActivity(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, user_id: int) -> responses.messages.GetLastActivity:
        """ messages.getLastActivity
        From Vk Docs: Returns a user's current status and date of last activity.
        Access from user token(s)
        :param user_id: User ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getLastActivity",
            params,
            response_model=responses.messages.GetLastActivityModel,
        )


class MessagesGetLongPollHistory(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        ts: int = None,
        pts: int = None,
        preview_length: int = None,
        onlines: bool = None,
        fields: typing.List = None,
        events_limit: int = None,
        msgs_limit: int = None,
        max_msg_id: int = None,
        group_id: int = None,
        lp_version: int = None,
        last_n: int = None,
        credentials: bool = None,
    ) -> responses.messages.GetLongPollHistory:
        """ messages.getLongPollHistory
        From Vk Docs: Returns updates in user's private messages.
        Access from user, group token(s)
        :param ts: Last value of the 'ts' parameter returned from the Long Poll server or by using [vk.com/dev/messages.getLongPollHistory|messages.getLongPollHistory] method.
        :param pts: Lsat value of 'pts' parameter returned from the Long Poll server or by using [vk.com/dev/messages.getLongPollHistory|messages.getLongPollHistory] method.
        :param preview_length: Number of characters after which to truncate a previewed message. To preview the full message, specify '0'. "NOTE: Messages are not truncated by default. Messages are truncated by words."
        :param onlines: '1' — to return history with online users only.
        :param fields: Additional profile [vk.com/dev/fields|fields] to return.
        :param events_limit: Maximum number of events to return.
        :param msgs_limit: Maximum number of messages to return.
        :param max_msg_id: Maximum ID of the message among existing ones in the local copy. Both messages received with API methods (for example, , ), and data received from a Long Poll server (events with code 4) are taken into account.
        :param group_id: Group ID (for group messages with user access token)
        :param lp_version: 
        :param last_n: 
        :param credentials: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getLongPollHistory",
            params,
            response_model=responses.messages.GetLongPollHistoryModel,
        )


class MessagesGetLongPollServer(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, need_pts: bool = None, group_id: int = None, lp_version: int = None
    ) -> responses.messages.GetLongPollServer:
        """ messages.getLongPollServer
        From Vk Docs: Returns data required for connection to a Long Poll server.
        Access from user, group token(s)
        :param need_pts: '1' — to return the 'pts' field, needed for the [vk.com/dev/messages.getLongPollHistory|messages.getLongPollHistory] method.
        :param group_id: Group ID (for group messages with user access token)
        :param lp_version: Long poll version
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.getLongPollServer",
            params,
            response_model=responses.messages.GetLongPollServerModel,
        )


class MessagesIsMessagesFromGroupAllowed(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, group_id: int, user_id: int
    ) -> responses.messages.IsMessagesFromGroupAllowed:
        """ messages.isMessagesFromGroupAllowed
        From Vk Docs: Returns information whether sending messages from the community to current user is allowed.
        Access from user, group token(s)
        :param group_id: Group ID.
        :param user_id: User ID.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.isMessagesFromGroupAllowed",
            params,
            response_model=responses.messages.IsMessagesFromGroupAllowedModel,
        )


class MessagesJoinChatByInviteLink(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(self, link: str) -> responses.messages.JoinChatByInviteLink:
        """ messages.joinChatByInviteLink
        From Vk Docs: 
        Access from user token(s)
        :param link: Invitation link.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.joinChatByInviteLink",
            params,
            response_model=responses.messages.JoinChatByInviteLinkModel,
        )


class MessagesMarkAsAnsweredConversation(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, peer_id: int, answered: bool = None, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ messages.markAsAnsweredConversation
        From Vk Docs: Marks and unmarks conversations as unanswered.
        Access from user, group token(s)
        :param peer_id: ID of conversation to mark as important.
        :param answered: '1' — to mark as answered, '0' — to remove the mark
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.markAsAnsweredConversation",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesMarkAsImportant(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, message_ids: typing.List = None, important: int = None
    ) -> responses.messages.MarkAsImportant:
        """ messages.markAsImportant
        From Vk Docs: Marks and unmarks messages as important (starred).
        Access from user token(s)
        :param message_ids: IDs of messages to mark as important.
        :param important: '1' — to add a star (mark as important), '0' — to remove the star
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.markAsImportant",
            params,
            response_model=responses.messages.MarkAsImportantModel,
        )


class MessagesMarkAsImportantConversation(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, peer_id: int, important: bool = None, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ messages.markAsImportantConversation
        From Vk Docs: Marks and unmarks conversations as important.
        Access from user, group token(s)
        :param peer_id: ID of conversation to mark as important.
        :param important: '1' — to add a star (mark as important), '0' — to remove the star
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.markAsImportantConversation",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesMarkAsRead(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        message_ids: typing.List = None,
        peer_id: int = None,
        start_message_id: int = None,
        group_id: int = None,
    ) -> responses.ok_response.OkResponse:
        """ messages.markAsRead
        From Vk Docs: Marks messages as read.
        Access from user, group token(s)
        :param message_ids: IDs of messages to mark as read.
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param start_message_id: Message ID to start from.
        :param group_id: Group ID (for group messages with user access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.markAsRead",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesPin(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, peer_id: int, message_id: int = None
    ) -> responses.messages.Pin:
        """ messages.pin
        From Vk Docs: Pin a message.
        Access from user, group token(s)
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'Chat ID', e.g. '2000000001'. For community: '- Community ID', e.g. '-12345'. "
        :param message_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.pin", params, response_model=responses.messages.PinModel
        )


class MessagesRemoveChatUser(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, chat_id: int, user_id: int = None, member_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ messages.removeChatUser
        From Vk Docs: Allows the current user to leave a chat or, if the current user started the chat, allows the user to remove another user from the chat.
        Access from user, group token(s)
        :param chat_id: Chat ID.
        :param user_id: ID of the user to be removed from the chat.
        :param member_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.removeChatUser",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesRestore(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, message_id: int, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ messages.restore
        From Vk Docs: Restores a deleted message.
        Access from user, group token(s)
        :param message_id: ID of a previously-deleted message to restore.
        :param group_id: Group ID (for group messages with user access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.restore",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesSearch(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        q: str = None,
        peer_id: int = None,
        date: int = None,
        preview_length: int = None,
        offset: int = None,
        count: int = None,
        extended: bool = None,
        fields: typing.List = None,
        group_id: int = None,
    ) -> responses.messages.Search:
        """ messages.search
        From Vk Docs: Returns a list of the current user's private messages that match search criteria.
        Access from user, group token(s)
        :param q: Search query string.
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param date: Date to search message before in Unixtime.
        :param preview_length: Number of characters after which to truncate a previewed message. To preview the full message, specify '0'. "NOTE: Messages are not truncated by default. Messages are truncated by words."
        :param offset: Offset needed to return a specific subset of messages.
        :param count: Number of messages to return.
        :param extended: 
        :param fields: 
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.search", params, response_model=responses.messages.SearchModel
        )


class MessagesSearchConversations(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        q: str = None,
        count: int = None,
        extended: bool = None,
        fields: typing.List = None,
        group_id: int = None,
    ) -> responses.messages.SearchConversations:
        """ messages.searchConversations
        From Vk Docs: Returns a list of the current user's conversations that match search criteria.
        Access from user, group token(s)
        :param q: Search query string.
        :param count: Maximum number of results.
        :param extended: '1' — return extra information about users and communities
        :param fields: Profile fields to return.
        :param group_id: Group ID (for group messages with user access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.searchConversations",
            params,
            response_model=responses.messages.SearchConversationsModel,
        )


class MessagesSend(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        user_id: int = None,
        random_id: int = None,
        peer_id: int = None,
        domain: str = None,
        chat_id: int = None,
        user_ids: typing.List = None,
        message: str = None,
        lat: typing.Any = None,
        long: typing.Any = None,
        attachment: str = None,
        reply_to: int = None,
        forward_messages: typing.List = None,
        forward: str = None,
        sticker_id: int = None,
        group_id: int = None,
        keyboard: str = None,
        payload: str = None,
        dont_parse_links: bool = None,
        disable_mentions: bool = None,
        expire_ttl: int = None,
        silent: bool = None,
        template: dict = None,
        intent: str = None,
    ) -> responses.messages.Send:
        """ messages.send
        From Vk Docs: Sends a message.
        Access from user, group token(s)
        :param user_id: User ID (by default — current user).
        :param random_id: Unique identifier to avoid resending the message.
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param domain: User's short address (for example, 'illarionov').
        :param chat_id: ID of conversation the message will relate to.
        :param user_ids: IDs of message recipients (if new conversation shall be started).
        :param message: (Required if 'attachments' is not set.) Text of the message.
        :param lat: Geographical latitude of a check-in, in degrees (from -90 to 90).
        :param long: Geographical longitude of a check-in, in degrees (from -180 to 180).
        :param attachment: (Required if 'message' is not set.) List of objects attached to the message, separated by commas, in the following format: "<owner_id>_<media_id>", '' — Type of media attachment: 'photo' — photo, 'video' — video, 'audio' — audio, 'doc' — document, 'wall' — wall post, '<owner_id>' — ID of the media attachment owner. '<media_id>' — media attachment ID. Example: "photo100172_166443618"
        :param reply_to: 
        :param forward_messages: ID of forwarded messages, separated with a comma. Listed messages of the sender will be shown in the message body at the recipient's. Example: "123,431,544"
        :param forward: 
        :param sticker_id: Sticker id.
        :param group_id: Group ID (for group messages with group access token)
        :param keyboard: 
        :param payload: 
        :param dont_parse_links: 
        :param disable_mentions: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.send", params, response_model=responses.messages.SendModel
        )


class MessagesSendService(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.GROUP,
        APIAccessibility.VKME,
    ]

    async def __call__(
        self, peer_id: int, action_type: str
    ) -> responses.ok_response.OkResponse:
        """ messages.sendService
        Still no docs in vk dox
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.sendService",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesSetActivity(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self,
        user_id: int = None,
        type: str = None,
        peer_id: int = None,
        group_id: int = None,
    ) -> responses.ok_response.OkResponse:
        """ messages.setActivity
        From Vk Docs: Changes the status of a user as typing in a conversation.
        Access from user, group token(s)
        :param user_id: User ID.
        :param type: 'typing' — user has started to type.
        :param peer_id: Destination ID. "For user: 'User ID', e.g. '12345'. For chat: '2000000000' + 'chat_id', e.g. '2000000001'. For community: '- community ID', e.g. '-12345'. "
        :param group_id: Group ID (for group messages with group access token)
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.setActivity",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesSetChatPhoto(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(self, file: str) -> responses.messages.SetChatPhoto:
        """ messages.setChatPhoto
        From Vk Docs: Sets a previously-uploaded picture as the cover picture of a chat.
        Access from user, group token(s)
        :param file: Upload URL from the 'response' field returned by the [vk.com/dev/photos.getChatUploadServer|photos.getChatUploadServer] method upon successfully uploading an image.
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.setChatPhoto",
            params,
            response_model=responses.messages.SetChatPhotoModel,
        )


class MessagesUnpin(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [
        APIAccessibility.USER,
        APIAccessibility.GROUP,
    ]

    async def __call__(
        self, peer_id: int, group_id: int = None
    ) -> responses.ok_response.OkResponse:
        """ messages.unpin
        From Vk Docs: 
        Access from user, group token(s)
        :param peer_id: 
        :param group_id: 
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.unpin",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class MessagesRecognizeAudioMessage(BaseMethod):
    kwargs: dict = {}
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, audio_message_id: str, message_id: int
    ) -> responses.ok_response.OkResponse:
        """ messages.recogniseAudioMessage
        Hidden method:
        :param audio_message_id: {owner_id}_{doc_id}
        :param message_id:
        """

        params = {
            k if not k.endswith("_") else k[:-1]: v
            for k, v in {**locals(), **self.kwargs}.items()
            if k not in ["self"] and v is not None
        }
        return await self.request(
            "messages.recogniseAudioMessage",
            params,
            response_model=responses.ok_response.OkResponseModel,
        )


class Messages:
    def __init__(self, request):
        self.add_chat_user = MessagesAddChatUser(request)
        self.allow_messages_from_group = MessagesAllowMessagesFromGroup(request)
        self.create_chat = MessagesCreateChat(request)
        self.delete = MessagesDelete(request)
        self.delete_chat_photo = MessagesDeleteChatPhoto(request)
        self.delete_conversation = MessagesDeleteConversation(request)
        self.deny_messages_from_group = MessagesDenyMessagesFromGroup(request)
        self.edit = MessagesEdit(request)
        self.edit_chat = MessagesEditChat(request)
        self.get_by_conversation_message_id = MessagesGetByConversationMessageId(
            request
        )
        self.get_by_id = MessagesGetById(request)
        self.get_chat_preview = MessagesGetChatPreview(request)
        self.get_conversation_members = MessagesGetConversationMembers(request)
        self.get_conversations = MessagesGetConversations(request)
        self.get_conversations_by_id = MessagesGetConversationsById(request)
        self.get_history = MessagesGetHistory(request)
        self.get_history_attachments = MessagesGetHistoryAttachments(request)
        self.get_invite_link = MessagesGetInviteLink(request)
        self.get_last_activity = MessagesGetLastActivity(request)
        self.get_long_poll_history = MessagesGetLongPollHistory(request)
        self.get_long_poll_server = MessagesGetLongPollServer(request)
        self.is_messages_from_group_allowed = MessagesIsMessagesFromGroupAllowed(
            request
        )
        self.join_chat_by_invite_link = MessagesJoinChatByInviteLink(request)
        self.mark_as_answered_conversation = MessagesMarkAsAnsweredConversation(request)
        self.mark_as_important = MessagesMarkAsImportant(request)
        self.mark_as_important_conversation = MessagesMarkAsImportantConversation(
            request
        )
        self.mark_as_read = MessagesMarkAsRead(request)
        self.pin = MessagesPin(request)
        self.remove_chat_user = MessagesRemoveChatUser(request)
        self.restore = MessagesRestore(request)
        self.search = MessagesSearch(request)
        self.search_conversations = MessagesSearchConversations(request)
        self.send = MessagesSend(request)
        self.send_service = MessagesSendService(request)
        self.set_activity = MessagesSetActivity(request)
        self.set_chat_photo = MessagesSetChatPhoto(request)
        self.unpin = MessagesUnpin(request)
        self.recognize_audio_message = MessagesRecognizeAudioMessage(request)
