<h1 align="center">VKBottle - high quality VK Tool</h1>
<p align="center">
    <blockquote>VKBottle - это многофункциональный модуль для работы с VK Api и создания ботов. Проект все еще тестируется на различных нагрузках</blockquote>
</p>
<hr>

## Установка
1) С помощью установщика pip из PyPi:
   
   Новейшая версия:
   ```sh
   pip install vkbottle
   ```
   
   Последний стабильный релиз:
   ```sh
   pip install vkbottle==2.7.1
   ```

2) С помощью установщика pip из GitHub: 
   
   ```sh
   pip install https://github.com/timoniq/vkbottle/archive/master.zip --upgrade
   ```
   
### Кастомизация

После установки `vkbottle` рекомендуется сразу же установить дополнительные модули `uvloop` и `loguru`, без них фреймворк работает медленне и логи не настраиваемы. О возможностях этих модулей можно прочитать в их документации

<a href="https://github.com/Delgan/loguru"><img alt="downloads" src="https://img.shields.io/static/v1?label=powered%20by&message=loguru&color=orange"></a>
<a href="https://github.com/MagicStack/uvloop"><img alt="downloads" src="https://img.shields.io/static/v1?label=powered%20by&message=uvloop&color=purple"></a>

Установите `uvloop` и `loguru` с помощью команд:

```sh
pip install loguru
pip install uvloop
```

Кроме того вы можете установить любую библиотеку для ускорения json из предложенных: `ujson`, `hyperjson`, `orjson`

### Фишки
- Удобная и быстрая доставка сообщений через regex
- Быстрый API враппер
- Быстрый LongPoll фреймворк для ботов
- Маленький объем кода со стороны пользователя
- Полностью асинхронно
- Ветки стейтов - Branches
- Блокирующая обработка - Middlewares
- Правила - Rules
- User LongPoll API

***

### Longpoll

```python
from vkbottle import Bot, Message

bot = Bot("my-token")


@bot.on.message(text="My name is <name>", lower=True)
async def wrapper(ans: Message, name):
    await ans("Hello, {}".format(name))


bot.run_polling(skip_updates=False)
```

### Callback

```python
from vkbottle import Bot, Message
from aiohttp import web

bot = Bot(token="my-token", secret="my-secret")
app = web.Application()


async def executor(request: web.Request):
    event = await request.json()
    emulation = await bot.emulate(event=event, confirmation_token="ConfirmationToken")
    return web.Response(text=emulation)


@bot.on.message(text="test", lower=True)
async def wrapper(ans: Message):
    return "Tested!"


app.router.add_route(
    path='/',
    method='POST',
    handler=executor
)
web.run_app(app=app, host=host, port=port)
```

### Rules

```python
from vkbottle import Bot, Message
from vkbottle.rule import AttachmentRule

bot = Bot("my-token")

@bot.on.message(AttachmentRule("photo"))
async def wrapper():
    return "What a beautiful photo!"
    
bot.run_polling()

```

### User LongPoll

```python
from vkbottle.user import User, Message

user = User("user-token")

@user.on.message_handler(text="can i ask you about <theme>?")
async def wrapper(ans: Message, theme: str):
    if theme in ["examples", "how to do smt", "depression", "insomnia"]:
        await ans("You can ask me about it in telegram @timoniq or make an issue on github!")
    else:
        await ans("Ok, sooner or later i ll respond you")

user.run_polling()
```

Больше примеров в папке [/examples](https://github.com/timoniq/vkbottle/tree/master/examples)

## Based on

[aiohttp](https://github.com/aio-libs/aiohttp) - longpoll и запросы к API  
[pydantic](https://github.com/samuelcolvin/pydantic) - все датаклассы  
[vbml](https://github.com/timoniq/vbml) - встроенная поддержка лучшего парсера сообщений

Для оптимальной работы фреймворка, рекомендуется использовать только [асинхронные библиотеки](https://github.com/timofurrer/awesome-asyncio)

## Contributing

ПР поддерживаются! Мне приятно видеть ваш вклад в развитие библиотеки  
Задавайте вопросы в блоке Issues и в чате VK!

## Лицензия

Copyright © 2019-2020 [timoniq](https://github.com/timoniq).  
Этот проект имеет GPL-3.0 лицензию.
