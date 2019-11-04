from ..types.message import Message
from ..api import Api, HandlerReturnError
from ..handler import Handler
from ..utils import Logger
from .patcher import Patcher
from .branch import BranchManager
from asyncio import AbstractEventLoop, ensure_future
from re import sub
from .regex import RegexHelper
from .branch import Branch, ExitBranch


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

        self._logger.debug(
            '-> MESSAGE FROM {} TEXT "{}" TIME %#%'.format(
                answer.from_id, answer.text.replace("\n", " ")
            )
        )

        for key in self.on.message.inner:
            if key.match(answer.text) is not None:
                matching = self.on.message.inner[key]

                validators_check = await self.patcher.check_validators(
                    check_object=matching, keys=key.match(answer.text).groupdict()
                )

                if validators_check is not None:
                    # [Feature] Async Use
                    # Added v0.19#master

                    task = await matching["call"](
                        *([answer] if not matching["ignore_ans"] else []),
                        **validators_check
                    )

                    self._logger.debug(
                        "New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                            matching["call"].__name__, answer.from_id
                        )
                    )
                    return task

        if self.on.undefined_func:
            await (self.on.undefined_func(answer))
            self._logger.debug(
                "New message compiled with decorator <\x1b[35mon-message-undefined\x1b[0m> (from: {})".format(
                    answer.from_id
                )
            )
        else:
            self._logger.info("Add on-undefined message handler!")

    async def _chat_message_processor(self, obj: dict, client_info: dict):
        """
        Chat messages processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        answer = Message(
            **{**obj, 'text': self.init_bot_mention(obj['text'])},
            api=[self.api],
            client_info=client_info
        )

        for key in self.on.chat_message.inner:
            if key.match(answer.text) is not None:

                self._logger.debug(
                    '-> MESSAGE FROM CHAT {} TEXT "{}" TIME %#%'.format(
                        answer.peer_id, answer.text.replace("\n", " ")
                    )
                )

                matching = self.on.chat_message.inner[key]

                validators_check = await self.patcher.check_validators(
                    check_object=matching, keys=key.match(answer.text).groupdict()
                )

                if validators_check is not None:
                    # [Feature] Async Use
                    # Added v0.19#master
                    task = await matching["call"](
                        *([answer] if not matching["ignore_ans"] else []),
                        **validators_check
                    )

                    self._logger.debug(
                        "New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                            matching["call"].__name__, answer.from_id
                        )
                    )
                    return task

    async def _chat_action_processor(self, obj: dict):
        """
        Chat Action Processor
        :param obj:
        :return: VK Server Event Object
        """

        action = obj["action"]

        self._logger.debug(
            '-> ACTION FROM CHAT {} TYPE "{}" TIME %#%'.format(
                obj["peer_id"], action["type"]
            ))

        for key in self.on.chat_action_types:
            rules = {**action, **key["rules"]}
            if action["type"] == key["name"] and rules == action:
                answer = Message(**obj, api=[self.api])

                await key["call"](answer)

                self._logger.debug(
                    "New action compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})".format(
                        key["call"].__name__,
                        answer.from_id,
                    ))
                break

    async def _event_processor(self, obj: dict, event_type: str):
        """
        LongPoll Events Processor
        :param event_type: VK Server Event Type
        :param obj: VK Server Event Object
        """

        self._logger.debug(
            '-> EVENT FROM {} TYPE "{}" TIME %#%'.format(
                obj["user_id"] if "user_id" in obj else "from_id", event_type.upper()
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
        task = ensure_future(self.branch.branches[branch[0]](answer, **branch[1]))

        task = await task

        self._logger.debug(
            "New BRANCHED-message compiled with branch <\x1b[35m{}\x1b[0m> (from: {})".format(
                branch, answer.from_id
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
            await Message(**obj, api=[self.api], client_info=client_info)(str(handler_return))
        elif handler_return is not None:
            raise HandlerReturnError(
                "Type {} can't be returned out of handler".format(
                    type(handler_return).__name__
                )
            )
