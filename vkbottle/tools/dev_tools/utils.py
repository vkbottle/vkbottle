from asyncio import get_running_loop
from typing import Coroutine, NoReturn


# This feature is not used in production
# but can be useful for customization
# purposes
def run_in_task(coroutine: Coroutine) -> NoReturn:
    loop = get_running_loop()
    loop.create_task(coroutine)
