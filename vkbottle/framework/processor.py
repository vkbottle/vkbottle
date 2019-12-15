from ..types.message import Message
from ..api import Api, HandlerReturnError
from ..handler import Handler
from ..utils import Logger
from .branch import BranchManager
from asyncio import AbstractEventLoop, ensure_future
from re import sub
from .regex import RegexHelper
from .branch import Branch, ExitBranch
from vbml import Pattern, Patcher
import typing
import json


def get_attr(adict: dict, attrs: typing.List[str]):
    attrs = set(attrs)
    for attr in attrs:
        if attr in adict:
            return adict[attr]


def redump_payload(payload: typing.Optional[str]) -> typing.Union[str, dict]:
    try:
        if payload:
            return json.loads(payload)
    except json.decoder.JSONDecodeError:
        return dict()


class EventProcessor(RegexHelper):
    api: Api
    on: Handler
    patcher: Patcher
    branch: BranchManager
    group_id: int
    _logger: Logger
    __loop: AbstractEventLoop

    async def _private_message_processor(self, obj: dict, client_info: dict):
        """
        Private message processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        answer = Message(**obj, api=[self.api], client_info=client_info)

        if self.on.pre:
            await (self.on.pre(answer))

        self._logger.debug(
            '-> MESSAGE FROM {} TEXT "{}" TIME %#%'.format(
                answer.from_id, answer.text.replace("\n", " ")
            )
        )
        found: bool = False

        # Payload alpha2
        redump = redump_payload(answer.payload)
        for pc in self.on.message.payload.inner:
            if pc(redump):
                matching = self.on.message.payload.inner[pc]
                task = await matching["call"](
                    *([answer] if not matching["ignore_ans"] else []))

                self._logger.debug(
                    "New message compiled with PAYLOAD decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        matching["call"].__name__, answer.from_id
                    )
                )
                return task

        for key in self.on.message.inner:
            key: Pattern
            if await self.patcher.check_async(answer.text, key) is not None:
                matching = self.on.message.inner[key]

                # [Feature] Async Use
                # Added v0.19#master

                task = await matching["call"](
                    *([answer] if not matching["ignore_ans"] else []), **key.dict()
                )

                self._logger.debug(
                    "New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        matching["call"].__name__, answer.from_id
                    )
                )
                found = True
                return task

        if not found:
            if self.on.undefined_func:
                task = await (self.on.undefined_func(answer))
                self._logger.debug(
                    "New message compiled with decorator <\x1b[35mon-message-undefined\x1b[0m> (from: {})".format(
                        answer.from_id
                    )
                )
                return task
            else:
                self._logger.info("Add on-undefined message handler!")

    async def _chat_message_processor(self, obj: dict, client_info: dict):
        """
        Chat messages processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        answer = Message(
            **{**obj, "text": self.init_bot_mention(obj["text"])},
            api=[self.api],
            client_info=client_info
        )

        if self.on.pre:
            ensure_future(self.on.pre(answer))

        # Payload alpha2
        redump = redump_payload(answer.payload)
        for pc in self.on.chat_message.payload.inner:
            if pc(redump):
                matching = self.on.chat_message.payload.inner[pc]
                task = await matching["call"](
                    *([answer] if not matching["ignore_ans"] else []))

                self._logger.debug(
                    "New message compiled with PAYLOAD decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        matching["call"].__name__, answer.from_id
                    )
                )
                return task

        for key in self.on.chat_message.inner:
            key: Pattern
            if await self.patcher.check_async(answer.text, key) is not None:

                self._logger.debug(
                    '-> MESSAGE FROM CHAT {} TEXT "{}" TIME %#%'.format(
                        answer.peer_id, answer.text.replace("\n", " ")
                    )
                )

                matching = self.on.chat_message.inner[key]

                # [Feature] Async Use
                # Added v0.19#master
                task = await matching["call"](
                    *([answer] if not matching["ignore_ans"] else []), **key.dict()
                )

                self._logger.debug(
                    "New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        matching["call"].__name__, answer.from_id
                    )
                )
                return task

    async def _chat_action_processor(self, obj: dict, client_info: dict):
        """
        Chat Action Processor
        :param obj:
        :return: VK Server Event Object
        """

        action = obj["action"]

        self._logger.debug(
            '-> ACTION FROM CHAT {} TYPE "{}" TIME %#%'.format(
                get_attr(obj, ["peer_id", "from_id"]), action["type"]
            )
        )

        for key in self.on.chat_action_types:
            rules = {**action, **key["rules"]}
            if action["type"] == key["name"] and rules == action:
                answer = Message(**obj, api=[self.api], client_info=client_info)

                await key["call"](answer)

                self._logger.debug(
                    "New action compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        key["call"].__name__, answer.from_id,
                    )
                )
                break

    async def _event_processor(self, obj: dict, event_type: str):
        """
        LongPoll Events Processor
        :param event_type: VK Server Event Type
        :param obj: VK Server Event Object
        """

        self._logger.debug(
            '-> EVENT FROM {} TYPE "{}" TIME %#%'.format(
                get_attr(obj, ["user_id", "from_id"]), event_type.upper()
            )
        )

        if event_type in self.on.event.events:
            event_processor = self.on.event.events[event_type]
            data = event_processor["data"](**obj, api=[self.api])

            await event_processor["call"](data)

            self._logger.debug(
                "New event compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                    event_processor["call"].__name__, "*"
                )
            )
            return True

    async def _branched_processor(self, obj: dict, client_info: dict):
        """
        Branched messages processor manager
        :param obj: VK Server Event Object
        """
        obj["text"] = sub(r"\[club" + str(self.group_id) + r"\|.*?\] ", "", obj["text"])

        answer = Message(**obj, api=[self.api], client_info=client_info)

        self._logger.debug(
            '-> BRANCHED MESSAGE FROM {} TEXT "{}" TIME %#%'.format(
                answer.peer_id, answer.text.replace("\n", " ")
            )
        )

        branch = self.branch.load(answer.peer_id)
        task = await (self.branch.branches[branch[0]](answer, **branch[1]))

        task = await self._handler_return(task, obj, client_info)
        _kw = str(branch[1])

        self._logger.debug(
            "New BRANCHED-message compiled with branch <\x1b[35m{}\x1b[0m> (from: {})".format(
                '"{}" with {} kwargs'.format(branch[0], _kw if len(_kw) < 100 else _kw[1:99]), answer.from_id
            )
        )
        return task

    async def _handler_return(self, handler_return, obj: dict, client_info: dict):
        """
        Allows use returns in handlers and operates them
        :param handler_return:
        :param obj:
        :return:
        """
        return_type = type(handler_return)
        if return_type in [Branch, ExitBranch]:
            if return_type == Branch:
                self._logger.mark("[Branch Collected]", handler_return.branch_name)
                self.branch.add(
                    obj["peer_id"],
                    handler_return.branch_name,
                    **handler_return.branch_kwargs
                )
            else:
                self._logger.mark("[Branch Exited]")
                self.branch.exit(obj["peer_id"])
        elif return_type in [str, int, dict, list, tuple, float]:
            await Message(**obj, api=[self.api], client_info=client_info)(
                str(handler_return)
            )
        elif handler_return is not None:
            raise HandlerReturnError(
                "Type {} can't be returned out of handler".format(
                    type(handler_return).__name__
                )
            )
