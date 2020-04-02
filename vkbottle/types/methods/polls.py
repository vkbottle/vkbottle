# Generated with love
import typing
import enum
from vkbottle.types import responses
from .access import APIAccessibility
from .method import BaseMethod


class PollsAddVote(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, poll_id: int, answer_ids: typing.List, is_board: bool
    ):
        """ polls.addVote
        From Vk Docs: Adds the current user's vote to the selected answer in the poll.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param poll_id: Poll ID.
        :param answer_ids: 
        :param is_board: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("polls.addVote", params)


class PollsCreate(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        question: str,
        is_anonymous: bool,
        is_multiple: bool,
        end_date: int,
        owner_id: int,
        add_answers: str,
        photo_id: int,
        background_id: str,
    ):
        """ polls.create
        From Vk Docs: Creates polls that can be attached to the users' or communities' posts.
        Access from user token(s)
        :param question: question text
        :param is_anonymous: '1' – anonymous poll, participants list is hidden,, '0' – public poll, participants list is available,, Default value is '0'.
        :param is_multiple: 
        :param end_date: 
        :param owner_id: If a poll will be added to a communty it is required to send a negative group identifier. Current user by default.
        :param add_answers: available answers list, for example: " ["yes","no","maybe"]", There can be from 1 to 10 answers.
        :param photo_id: 
        :param background_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("polls.create", params)


class PollsDeleteVote(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self, owner_id: int, poll_id: int, answer_id: int, is_board: bool
    ):
        """ polls.deleteVote
        From Vk Docs: Deletes the current user's vote from the selected answer in the poll.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param poll_id: Poll ID.
        :param answer_id: Answer ID.
        :param is_board: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("polls.deleteVote", params)


class PollsEdit(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        poll_id: int,
        question: str,
        add_answers: str,
        edit_answers: str,
        delete_answers: str,
        end_date: int,
        photo_id: int,
        background_id: str,
    ):
        """ polls.edit
        From Vk Docs: Edits created polls
        Access from user token(s)
        :param owner_id: poll owner id
        :param poll_id: edited poll's id
        :param question: new question text
        :param add_answers: answers list, for example: , "["yes","no","maybe"]"
        :param edit_answers: object containing answers that need to be edited,, key – answer id, value – new answer text. Example: {"382967099":"option1", "382967103":"option2"}"
        :param delete_answers: list of answer ids to be deleted. For example: "[382967099, 382967103]"
        :param end_date: 
        :param photo_id: 
        :param background_id: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("polls.edit", params)


class PollsGetById(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        is_board: bool,
        poll_id: int,
        extended: bool,
        friends_count: int,
        fields: typing.List,
        name_case: str,
    ):
        """ polls.getById
        From Vk Docs: Returns detailed information about a poll by its ID.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param is_board: '1' – poll is in a board, '0' – poll is on a wall. '0' by default.
        :param poll_id: Poll ID.
        :param extended: 
        :param friends_count: 
        :param fields: 
        :param name_case: 
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("polls.getById", params)


class PollsGetVoters(BaseMethod):
    access_token_type: APIAccessibility = [APIAccessibility.USER]

    async def __call__(
        self,
        owner_id: int,
        poll_id: int,
        answer_ids: typing.List,
        is_board: bool,
        friends_only: bool,
        offset: int,
        count: int,
        fields: typing.List,
        name_case: str,
    ):
        """ polls.getVoters
        From Vk Docs: Returns a list of IDs of users who selected specific answers in the poll.
        Access from user token(s)
        :param owner_id: ID of the user or community that owns the poll. Use a negative value to designate a community ID.
        :param poll_id: Poll ID.
        :param answer_ids: Answer IDs.
        :param is_board: 
        :param friends_only: '1' — to return only current user's friends, '0' — to return all users (default),
        :param offset: Offset needed to return a specific subset of voters. '0' — (default)
        :param count: Number of user IDs to return (if the 'friends_only' parameter is not set, maximum '1000', otherwise '10'). '100' — (default)
        :param fields: Profile fields to return. Sample values: 'nickname', 'screen_name', 'sex', 'bdate (birthdate)', 'city', 'country', 'timezone', 'photo', 'photo_medium', 'photo_big', 'has_mobile', 'rate', 'contacts', 'education', 'online', 'counters'.
        :param name_case: Case for declension of user name and surname: , 'nom' — nominative (default) , 'gen' — genitive , 'dat' — dative , 'acc' — accusative , 'ins' — instrumental , 'abl' — prepositional
        """

        params = {k: v for k, v in locals().items() if k not in ["self"]}
        return await self.request("polls.getVoters", params)


class Polls:
    def __init__(self, request):
        self.add_vote = PollsAddVote(request)
        self.create = PollsCreate(request)
        self.delete_vote = PollsDeleteVote(request)
        self.edit = PollsEdit(request)
        self.get_by_id = PollsGetById(request)
        self.get_voters = PollsGetVoters(request)
