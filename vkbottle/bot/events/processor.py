"""Read LICENSE.txt"""


from ...vktypes.longpoll import EventTypes

from ...methods import Api

from ..events import Events

from ...utils import Logger, sorted_dict_keys

import time

from ...vktypes import types

from ...project_collections import colored

from ..patcher import Patcher


class UpdatesProcessor(object):
    """
    Processor of VK API LongPoll events
    """
    on: Events
    logger: Logger
    api: Api
    a: float
    patcher: Patcher

    async def new_update(self, event: dict):
        """
        Process VK Event Object
        :param event: VK Server Event object
        """

        for update in event['updates']:

            obj = update['object']

            if await self.patcher.check_for_whitelist(obj):

                if update['type'] == EventTypes.MESSAGE_NEW:

                    if obj['peer_id'] < 2e9:
                        await self.new_message(obj=obj)

                    else:
                        if 'action' not in obj:
                            await self.new_chat_message(obj=obj)
                        else:
                            await self.new_chat_action(obj=obj)

                else:
                    # If this is an event of the group
                    await self.new_event(event_type=update['type'], obj=obj)

    async def new_message(self, obj: dict):
        """
        Private message processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        await self.logger(
            colored(
                '-> MESSAGE FROM {} TEXT "{}" TIME #'.format(
                    obj['peer_id'],
                    obj['text'].replace('\n', ' / ')
            ),
                'red'
            )
        )

        answer = types.Message(**obj, api=[self.api])
        found: bool = False

        for priority in await sorted_dict_keys(self.on.processor_message_regex):

            for key in self.on.processor_message_regex[priority]:

                if key.match(answer.text) is not None:

                    found = True
                    keys = key.match(answer.text).groupdict()

                    validators_check = await self.patcher.check_validators(
                        check_object=self.on.processor_message_regex[priority][key],
                        keys=keys)

                    if validators_check:
                        # [Feature] Async Use
                        # Added v0.19#master
                        await self.on.processor_message_regex[priority][key]['call'](
                            answer,
                            **validators_check
                        )

                        await self.logger(
                            'New message compiled with decorator <' +
                            colored(self.on.processor_message_regex[priority][key]['call'].__name__, 'magenta') +
                            '> (from: {})'.format(
                                answer.from_id
                            ),
                            '>>', round(time.time() - self.a, 5)
                        )

                        break
                    continue

            if found:
                break

        if not found:
            await self.on.undefined_message_func(answer)

    async def new_chat_message(self, obj: dict):
        """
        Chat messages processor. Using regex to process regular expressions in messages
        :param obj: VK API Event Object
        """

        await self.logger(
            colored(
                '-> MESSAGE FROM CHAT {} TEXT "{}" TIME #'.format(
                    obj['peer_id'],
                    obj['text'].replace('\n', ' ')
                ),
                'red'
            ))

        answer = types.Message(**obj, api=[self.api])
        found: bool = False

        for priority in await sorted_dict_keys(self.on.processor_message_chat_regex):

            for key in self.on.processor_message_regex[priority]:

                if key.match(answer.text) is not None:

                    found = True
                    keys = key.match(answer.text).groupdict()

                    validators_check = await self.patcher.check_validators(
                        check_object=self.on.processor_message_chat_regex[priority][key],
                        keys=keys)

                    if validators_check:
                        # [Feature] Async Use
                        # Added v0.19#master
                        await self.on.processor_message_chat_regex[priority][key]['call'](
                            answer,
                            **validators_check
                        )

                        await self.logger(
                            'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                                self.on.processor_message_chat_regex[priority][key]['call'].__name__,
                                answer.from_id
                            ),
                            '>>', round(time.time() - self.a, 5)
                        )

                        break
                    continue

            if found:
                break

    async def new_event(self, event_type: str, obj: dict):
        """
        LongPoll Events Processor
        :param event_type: VK Server Event Type
        :param obj: VK Server Event Object
        """
        await self.logger(
            colored(
                '-> EVENT FROM {} TYPE "{}" TIME #'.format(
                    obj['from_id'],
                    event_type.upper()
                ),
                'red'
            ))

        if event_type in self.on.events:
            event_processor = self.on.events[event_type]
            data = event_processor['data'](**obj, api=[self.api])

            await event_processor['call'](data)

            await self.logger(
                'New message compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                    event_processor['call'].__name__,
                    data.from_id
                ),
                '>>', round(time.time() - self.a, 5)
            )

    async def new_chat_action(self, obj: dict):
        """
        Chat Action Processor
        :param obj:
        :return: VK Server Event Object
        """
        action = obj['action']

        await self.logger(
            colored(
                '-> ACTION FROM CHAT {} TYPE "{}" TIME #'.format(
                    obj['peer_id'],
                    action['type']
                ),
                'red'
            ))

        if action['type'] in self.on.chat_action_types:
            if {**action, **self.on.chat_action_types[action['type']]['rules']} == action:
                answer = types.Message(**obj, api=[self.api])

                await self.on.chat_action_types[action['type']]['call'](answer)

                await self.logger(
                    'New action compiled with decorator <\x1b[35m{}\x1b[0m> (from: {})'.format(
                        self.on.chat_action_types[action['type']]['call'].__name__,
                        answer.from_id
                    ),
                    '>>', round(time.time() - self.a, 5)
                )
