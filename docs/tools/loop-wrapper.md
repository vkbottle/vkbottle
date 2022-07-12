# Loop Wrapper

`LoopWrapper` нужен чтобы контролировать ивент луп для работы с `asyncio` и хранить основные таски, `startup` и `shutdown`, которые будут исполнены только при запуске ивент лупа через `run_forever`

Если вы установите `loop_wrapper.auto_reload = True`, то программа будет автоматически перезагружаться при изменениях в кодe, чтобы указать путь до вашего кода воспользуйтесь `auto_reload_dir`, по умолчанию он локален

## Таски

Вы можете создать таск так:

```python
from vkbottle import LoopWrapper

async def my_task():
    ...

lw = LoopWrapper()
lw.add_task(my_task())
```

## on_startup и on_shutdown

`on_startup` корутины запустятся перед запуском ивент лупа, `on_shutdown` при остановке. В экземпляре `LoopWrapper` они являются списками с корутинами, следовательно, добавлять их можно так:

```python
from vkbottle import LoopWrapper

async def startup_task():
    print("This is startup")

async def shutdown_task():
    print("This is shutdown")

lw = LoopWrapper()
lw.on_startup.append(startup_task())
lw.on_shutdown.append(shutdown_task())
```

## interval

Легкий темплейт для создания тасков с бесконечно повторяющимися действиями в интервале. Пример:

```python
from vkbottle import LoopWrapper

lw = LoopWrapper()

@lw.interval(seconds=10)
async def repeated_task():
    print("I'll print this every 10 seconds!")
```

## timer

Легкий темплейт для создания отложенного таска:

```python
from vkbottle import LoopWrapper

lw = LoopWrapper()

@lw.timer(seconds=10)
async def delayed_task():
    print("I'll print this after 10 seconds!")
```

## Запуск

```python
lw.run_forever()
```

!!! warning "Внимание"
    Если вы используете `LoopWrapper` вместе с `Bot`, то учтите, то `Bot` уже имеет свой `LoopWrapper`, который доступен по пути `bot.loop_wrapper` и запускается при вызове `bot.run_forever()`
