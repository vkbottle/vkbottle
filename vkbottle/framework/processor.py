import typing, types
from asyncio import AbstractEventLoop
from re import sub
from ..utils import logger

from vbml import Patcher

from ..types.message import Message
from ..api import Api
from ..handler import Handler
from ..handler.middleware import MiddlewareExecutor
from .branch import BranchManager
from .regex import RegexHelper
from .branch import Branch, ExitBranch
from ._status import BotStatus


def get_attr(adict: dict, attrs: typing.List[str]):
    attrs = set(attrs)
    for attr in attrs:
        if attr in adict:
            return adict[attr]
    return None


class EventProcessor(RegexHelper):
    api: Api
    on: Handler
    middleware: MiddlewareExecutor
    patcher: Patcher
    branch: BranchManager
    status: BotStatus
    group_id: int
    loop: AbstractEventLoop

    async def _processor(self, obj: dict, client_info: dict):
        processor = dict(obj=obj, client_info=client_info)

        message = Message(
            **{**obj, "text": self.init_bot_mention(obj["text"])},
            client_info=client_info
        )

        async for mr in self.middleware.run_middleware(message):
            if self.status.middleware_expressions:
                if mr is False:
                    return

        if message.from_id in self.branch.queue or message.peer_id in self.branch.queue:
            await self._branched_processor(obj, client_info)
            return

        logger.debug(
            '-> MESSAGE FROM {} TEXT "{}"',
            message.from_id,
            message.text.replace("\n", " "),
        )

        task = None
        for rules in self.on.rules:

            for rule in rules:
                if not await rule(message):
                    break

            else:

                args = [a for rule in rules for a in rule.context.args]
                kwargs = {
                    k: v for rule in rules for k, v in rule.context.kwargs.items()
                }
                if not getattr(rules[0], "data", {}).get("ignore_ans"):
                    args = [message, *args]

                task = await rules[0].call(*args, **kwargs)

                logger.info(
                    'New message "{}" compiled with decorator <{}> (from: {}/{})'.format(
                        message.text.replace("\n", " "),
                        rules[0].call.__name__,
                        message.peer_id,
                        message.from_id,
                    )
                )
                break

        await self._handler_return(task, **processor)

    async def _event_processor(self, obj: dict, event_type: str):
        """
        LongPoll Events Processor
        :param event_type: VK Server Event Type
        :param obj: VK Server Event Object
        """

        logger.debug(
            '-> EVENT FROM {} TYPE "{}"',
            get_attr(obj, ["user_id", "from_id"]),
            event_type.upper(),
        )

        for rule in self.on.event.rules:
            if await rule.check(event_type):
                event = rule.data["data"](**obj)
                await rule.call(event, *rule.context.args, **rule.context.kwargs)

                logger.info(
                    'New event "{}" compiled with decorator <{}> (from: {})'.format(
                        event_type.upper(),
                        rule.call.__name__,
                        get_attr(obj, ["user_id", "from_id"]),
                    )
                )
                return True

    async def _branched_processor(self, obj: dict, client_info: dict):
        """
        Branched messages processor manager
        :param obj: VK Server Event Object
        """
        obj["text"] = sub(r"\[club" + str(self.group_id) + r"\|.*?\] ", "", obj["text"])

        answer = Message(**obj, client_info=client_info)

        logger.debug(
            '-> BRANCHED MESSAGE FROM {} TEXT "{}"',
            answer.peer_id,
            answer.text.replace("\n", " "),
        )

        disposal, branch = await self.branch.load(answer.peer_id)
        await branch.enter(answer)

        for n, member in disposal.items():
            rules = member[1]
            for rule in rules:
                if not await rule(answer):
                    break
            else:
                task = types.MethodType(member[0], branch)
                args = [a for rule in rules for a in rule.context.args]
                kwargs = {
                    k: v for rule in rules for k, v in rule.context.kwargs.items()
                }
                await self._handler_return(await task(answer, *args, **kwargs), obj, client_info)
                break

        logger.info(
            'New BRANCHED "{0}" compiled with branch <{2}> (from: {1})'.format(
                answer.text.replace("\n", " "),
                answer.from_id,
                '"{}" with {} kwargs'.format(
                    branch.key,
                    branch.context
                    if len(branch.context) < 100
                    else branch.context[1:99] + "...",
                ),
            )
        )
        await branch.exit(answer)

    async def _handler_return(self, handler_return, obj: dict, client_info: dict):
        """
        Allows use returns in handlers and operates them
        :param handler_return:
        :param obj:
        :return:
        """
        if isinstance(handler_return, Branch):
            self.branch.add(
                obj["peer_id"],
                handler_return.branch_name,
                **handler_return.branch_kwargs
            )
        elif isinstance(handler_return, ExitBranch):
            self.branch.exit(obj["peer_id"])
        elif handler_return is not None:
            await Message(**obj, client_info=client_info)(
                str(handler_return), **self.status.handler_return_context
            )
