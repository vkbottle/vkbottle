import types
from re import sub

from vkbottle.framework.framework.branch import Branch, ExitBranch
from vkbottle.framework.framework.branch import GeneratorType
from vkbottle.framework.framework.handler import MiddlewareFlags
from vkbottle.types.events import EventList
from vkbottle.types.message import Message
from vkbottle.utils import logger, init_bot_mention
from vkbottle.utils.exceptions import VKError
from vkbottle.utils.tools import get_attr
from ..framework.swear_handler import swear
from ..processor import ABCProcessor


class BotProcessor(ABCProcessor):
    def __init__(self, group_id: int):
        self.group_id = group_id

    @swear(Exception, just_log=True)
    async def parent_processor(self, update: dict, obj: dict):
        """ Classify and distribute user polling events as message and not message
        #TODO Reduce difference
        :param update: full event
        :param obj: update object
        """
        if update["type"] == EventList.MESSAGE_NEW:

            # VK API v5.103
            client_info = obj.get("client_info")
            if client_info is None:
                raise VKError(0, "Change API version to 5.103 or later") from None
            obj = obj["message"]

            return await self.message_processor(obj, client_info)
        return await self.event_processor(obj=obj, event_type=update["type"])

    async def message_processor(self, obj: dict, client_info: dict):
        processor = dict(object=obj, client_info=client_info)
        middleware_args = []

        message = Message(
            **{**obj, "text": init_bot_mention(self.group_id, obj["text"])},
            client_info=client_info,
        )
        branch_checkup_key = message.dict()[self.branch.checkup_key.value]

        async for mr in self.middleware.run_middleware(
            message, flag=MiddlewareFlags.PRE
        ):
            if self.status.middleware_expressions:
                if mr is False:
                    return
                elif mr is not None:
                    middleware_args.append(mr)

        if branch_checkup_key in await self.branch.queue:
            await self.branch_processor(obj, client_info, middleware_args)
            return

        logger.debug(
            '-> MESSAGE FROM {} TEXT "{}"',
            message.from_id,
            message.text.replace("\n", " "),
        )

        for rules in self.handler.message_rules:

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
                await self.handler_return(task, data=processor)

                logger.info(
                    'New message "{}" compiled with decorator <{}> (from: {}/{})'.format(
                        message.text.replace("\n", " "),
                        rules[0].call.__name__,
                        message.peer_id,
                        message.from_id,
                    )
                )
                break

        async for mr in self.middleware.run_middleware(
            message, MiddlewareFlags.POST, *middleware_args
        ):
            logger.debug(f"POST Middleware handler returned: {mr}")

    async def event_processor(self, obj: dict, event_type: str):
        """ Bot polling event processor
        #TODO Reduce difference
        :param event_type: VK Server Event Type
        :param obj: VK Server Event Object
        """

        logger.debug(
            '-> EVENT FROM {} TYPE "{}"',
            get_attr(obj, ["user_id", "from_id"]),
            event_type.upper(),
        )

        for rule in self.handler.event.rules:
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
                break

    async def branch_processor(
        self, obj: dict, client_info: dict, middleware_args: list
    ):
        """ Process messages for users in branch storage
        #TODO Make a simple branch extendable processor
        #TODO Move middleware_args
        """
        obj["text"] = sub(r"\[club" + str(self.group_id) + r"\|.*?\] ", "", obj["text"])

        message = Message(**obj, client_info=client_info)
        branch_checkup_key = message.dict()[self.branch.checkup_key.value]

        logger.debug(
            '-> BRANCHED MESSAGE FROM {} TEXT "{}"',
            message.peer_id,
            message.text.replace("\n", " "),
        )

        disposal, branch = await self.branch.load(branch_checkup_key)
        edited = None

        for n, member in disposal.items():
            rules = member[1]
            for rule in rules:
                if not await rule(message):
                    break
            else:
                task = types.MethodType(member[0], branch)
                args = [a for rule in rules for a in rule.context.args]
                kwargs = {
                    k: v for rule in rules for k, v in rule.context.kwargs.items()
                }
                edited = await self.handler_return(
                    await task(message, *middleware_args, *args, **kwargs),
                    data={"object": obj, "client_info": client_info},
                )
                break

        # FIXME
        if (
            edited is False
            and self.branch.__class__.generator is GeneratorType.DATABASE
        ):
            if branch_checkup_key in await self.branch.queue:
                logger.debug("Updating branch context")
                await self.branch.add(branch_checkup_key, branch.key, **branch.context)

        logger.info(
            'New BRANCHED "{0}" compiled with branch <{2}> (from: {1})'.format(
                message.text.replace("\n", " "), message.from_id, repr(branch.key),
            )
        )

    async def handler_return(self, handler_return, data: dict) -> bool:
        """ Allows use returns in handlers and operates them
        #TODO (issue #84) make handler return manager
        :param handler_return:
        :param data:
        :return:
        """
        obj, client_info = data["object"], data["client_info"]

        if isinstance(handler_return, Branch):
            await self.branch.add(
                obj["peer_id"],
                handler_return.branch_name,
                **handler_return.branch_kwargs,
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
