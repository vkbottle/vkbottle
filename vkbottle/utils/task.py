import asyncio
from asyncio import iscoroutinefunction
from typing import List, Callable


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


class TaskQueue:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.tasks: List[Callable] = []
        self.loop: asyncio.AbstractEventLoop = loop

    def run(
        self,
        shutdown: Callable = None,
        startup: Callable = None,
        asyncio_debug_mode: bool = False,
    ):
        """
        Run events
        """
        if len(self.tasks) < 1:
            raise RuntimeError("Count of tasks - 0. Add tasks.")
        try:
            if startup is not None:
                self.loop.run_until_complete(startup())

            if asyncio_debug_mode:
                self.loop.set_debug(True)

            [self.loop.create_task(task()) for task in self.tasks]

            self.loop.run_forever()

        finally:
            if shutdown is not None:
                self.loop.run_until_complete(shutdown())

    def close(self):
        """
        Close event loop manually
        :return:
        """
        self.loop.close()

    def add_task(self, task: Callable):
        """
        Add task to loop when loop don`t started.
        :param task: coroutine for run in loop
        :return:
        """
        if iscoroutinefunction(task):
            self.tasks.append(task)
        else:
            raise RuntimeError("Unexpected task. Tasks may be only coroutine functions")

    def run_task(self, task: Callable):
        """
        Create task in loop
        :param task:
        :return:
        """

        self.loop.create_task(task())
