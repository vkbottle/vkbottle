import types
from asyncio import AbstractEventLoop
from re import sub
from vkbottle.utils import logger, init_bot_mention

from vbml import Patcher

from vkbottle.types.message import Message
from vkbottle.api import Api
from vkbottle.framework.framework.handler.handler import Handler
from vkbottle.framework.framework.handler import MiddlewareExecutor
from vkbottle.framework.framework.branch import AbstractBranchGenerator, GeneratorType
from vkbottle.framework.framework.branch import Branch, ExitBranch
from vkbottle.framework._status import BotStatus
from vkbottle.utils.tools import get_attr


class AsyncHandleManager:
    api: Api
    on: Handler
    middleware: MiddlewareExecutor
    patcher: Patcher
    branch: AbstractBranchGenerator
    status: BotStatus
    group_id: int
    loop: AbstractEventLoop

    async def _processor(self, obj: dict, client_info: dict):
        processor = dict(obj=obj, client_info=client_info)
        middleware_args = []

        message = Message(
            **{**obj, "text": init_bot_mention(self.group_id, obj["text"])},
            client_info=client_info
        )

        async for mr in self.middleware.run_middleware(message):
            if self.status.middleware_expressions:
                if mr is False:
                    return
                elif mr is not None:
                    middleware_args.append(mr)

        if message.peer_id in await self.branch.queue:
            await self._branched_processor(obj, client_info, middleware_args)
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

                args = [message, *middleware_args, *args]

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

    async def _branched_processor(
        self, obj: dict, client_info: dict, middleware_args: list
    ):
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
        edited = None

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
                edited = await self._handler_return(
                    await task(answer, *middleware_args, *args, **kwargs),
                    obj,
                    client_info,
                )
                break

        if edited is False and self.branch.generator is GeneratorType.DATABASE:
            if answer.peer_id in await self.branch.queue:
                await self.branch.add(answer.peer_id, branch.key, **branch.context)

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

    async def _handler_return(
        self, handler_return, obj: dict, client_info: dict
    ) -> bool:
        """
        Allows use returns in handlers and operates them
        :param handler_return:
        :param obj:
        :return:
        """
        if isinstance(handler_return, Branch):
            await self.branch.add(
                obj["peer_id"],
                handler_return.branch_name,
                **handler_return.branch_kwargs
            )
            return True
        elif isinstance(handler_return, ExitBranch):
            await self.branch.exit(obj["peer_id"])
            return True
        elif handler_return is not None:
            await Message(**obj, client_info=client_info)(
                str(handler_return), **self.status.handler_return_context
            )
        return False
