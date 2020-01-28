# TaskManager

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
