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
from ._status import BotStatus


def get_attr(adict: dict, attrs: typing.List[str]):
    attrs = set(attrs)
    for attr in attrs:
        if attr in adict:
            return adict[attr]


class EventProcessor(RegexHelper):
    api: Api
    on: Handler
    patcher: Patcher
    branch: BranchManager
    status: BotStatus
    group_id: int
    _logger: Logger
    __loop: AbstractEventLoop

    async def _private_message_processor(self, obj: dict, client_info: dict):
        """
        Private message processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        message = Message(**obj, api=[self.api], client_info=client_info)

        if self.on.pre:
            await (self.on.pre(message))

        self._logger.debug(
            '-> MESSAGE FROM {} TEXT "{}" TIME %#%'.format(
                message.from_id, message.text.replace("\n", " ")
            )
        )

        for rules in [*self.on.message.payload.rules, *self.on.message.rules]:
            if all([rule.check(message) for rule in rules]):
                args = [a for rule in rules for a in rule.context.args]
                kwargs = {k: v for rule in rules for k, v in rule.context.kwargs.items()}
                if not rules[0].data.get("ignore_ans"):
                    args = [message, *args]

                task = await rules[0].call(*args, **kwargs)

                self._logger.debug(
                    "New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        rules[0].call.__name__, message.from_id
                    )
                )

                return task

        if self.on.undefined_func:
            task = await (self.on.undefined_func(message))
            self._logger.debug(
                "New message compiled with decorator <\x1b[35mon-message-undefined\x1b[0m> (from: {})".format(
                    message.from_id
                )
            )
            return task
        else:
            self._logger.info(
                "Add on-undefined message handler to persue group online!"
            )

    async def _chat_message_processor(self, obj: dict, client_info: dict):
        """
        Chat messages processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        message = Message(
            **{**obj, "text": self.init_bot_mention(obj["text"])},
            api=[self.api],
            client_info=client_info
        )

        if self.on.pre:
            await (self.on.pre(message))

        for rules in [*self.on.chat_message.payload.rules, *self.on.chat_message.rules]:
            if all([rule.check(message) for rule in rules]):
                args = [a for rule in rules for a in rule.context.args]
                kwargs = {k: v for rule in rules for k, v in
                          rule.context.kwargs.items()}
                if not rules[0].data.get("ignore_ans"):
                    args = [message, *args]

                self._logger.debug(
                    '-> MESSAGE FROM CHAT {} TEXT "{}" TIME %#%'.format(
                        message.peer_id, message.text.replace("\n", " ")
                    )
                )

                task = await rules[0].call(*args, **kwargs)

                self._logger.debug(
                    "New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        rules[0].call.__name__, message.from_id
                    )
                )

                return task

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

        for rule in self.on.event.rules:
            if rule.check(event_type):
                event = rule.data["data"](**obj, api=[self.api])
                await rule.call(event, *rule.context.args, **rule.context.kwargs)

                self._logger.debug(
                    "New event compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        rule.call.__name__, "*"
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
                '"{}" with {} kwargs'.format(
                    branch[0], _kw if len(_kw) < 100 else _kw[1:99] + "..."
                ),
                answer.from_id,
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
                str(handler_return), **self.status.handler_return_context
            )
        elif handler_return is not None:
            raise HandlerReturnError(
                "Type {} can't be returned out of handler".format(
                    type(handler_return).__name__
                )
            )
