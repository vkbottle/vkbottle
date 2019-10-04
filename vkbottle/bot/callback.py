from ..utils import task_queue
import asyncio
import queue


class WebHook(object):
    """Manage webhook in the event queues
    """
    WEBHOOK_URL = '1.1.1.1'


class CallBack(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.tasks: task_queue.Queue = task_queue.Queue(self.loop)
        self._webhook = WebHook()
