# TaskManager

С помощью `TaskManager` можно запустить мультисессию и бекграунд таски  

```python
from vkbottle import Bot, User, TaskManager
import asyncio

bot = Bot("token")
user = User("user-token")

async def startup_action():
    print("Oo! Raised before bot has started")
    # do stuff

async def background_task():
    await asyncio.sleep(100)
    print("Oo! Background task. Here you can update smt for instance")
    # do stuff

tm = TaskManager()
tm.add_task(bot.run(skip_updates=False))
tm.add_task(user.run)
tm.add_task(background_task())
tm.run(on_startup=startup_action())
```

Import:

```python
from vkbottle import TaskManager
manager = TaskManager() # if you don't have running loop
manager = TaskManager(bot.loop) # if you have initialized bot
# ...
```

Use of manager:

`manager.add_task(task: Coroutine or Callable)` - add task to the queue, queue can be started with `manager.run()`  

`manager.run_task(task: Coroutine or Callable)` - run task, ignore queue  

`manager.run()` - run tasks in queue in `loop.run_forever`  

`manager.close()` - close event loop
