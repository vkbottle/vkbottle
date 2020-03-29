import asyncio
import typing

from ..utils.logger import logger
from .auto_reload import _auto_reload


"""
MIT License

Copyright (c) 2019 prostomarkeloff

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class TaskManager:
    """
    Task manager represent to user high-level API of asyncio interface (Less part :))
    """

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.tasks: typing.List[typing.Callable] = []
        self.loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()

    def run(
        self,
        *,
        on_shutdown: typing.Callable = None,
        on_startup: typing.Callable = None,
        auto_reload: bool = False,
        auto_reload_dir: str = ".",
        asyncio_debug_mode: bool = False,
    ):
        """
        Method which run event loop
        :param auto_reload: auto reload code when changes
        :param on_shutdown: coroutine which runned after complete tasks
        :param on_startup: coroutine which runned before start main tasks
        :param auto_reload_dir:
        :param asyncio_debug_mode: asyncio debug mode state
        :return:
        """
        if len(self.tasks) < 1:
            raise RuntimeError("Count of tasks - 0. Add tasks.")
        try:
            if on_startup is not None:
                self.loop.run_until_complete(on_startup())

            if asyncio_debug_mode:
                self.loop.set_debug(True)

            if auto_reload:
                self.loop.create_task(_auto_reload(auto_reload_dir))

            [self.loop.create_task(task) for task in self.tasks]

            self.loop.run_forever()

        except KeyboardInterrupt:
            logger.info("Keyboard Interrupt")
            exit(0)

        finally:
            if on_shutdown is not None:
                self.loop.run_until_complete(on_shutdown())
            self.close()

    def close(self):
        """
        Close event loop manually
        :return:
        """
        self.loop.close()

    def add_task(self, task: typing.Union[typing.Coroutine, typing.Callable]):
        """
        Add task to loop when loop don`t started.
        :param task: coroutine for run in loop
        :return:
        """
        if asyncio.iscoroutinefunction(task):
            self.tasks.append(task())
        elif asyncio.iscoroutine(task):
            self.tasks.append(task)
        else:
            raise RuntimeError("Unexpected task. Tasks may be only coroutine functions")

    def run_task(self, task: typing.Union[typing.Coroutine, typing.Callable]):
        """
        Create task in loop
        :param task:
        :return:
        """

        if asyncio.iscoroutinefunction(task):
            self.loop.create_task(task())
        elif asyncio.iscoroutine(task):
            self.loop.create_task(task)
        else:
            raise RuntimeError("Unexpected task. Tasks may be only coroutine functions")
