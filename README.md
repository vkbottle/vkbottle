<h1 align="center">VKBottle - high quality VK Tool</h1>
<p align="center"><a href="https://pypi.org/project/vkbottle/"><img alt="downloads" src="https://img.shields.io/static/v1?label=pypi%20package&message=2.4&color=brightgreen"></a> <a href="https://github.com/timoniq/vkbottle"><img src="https://img.shields.io/static/v1?label=version&message=opensource&color=green" alt="service-test status"></a> <a href="https://vk.me/join/AJQ1d7fBUBM_800lhEe_AwJj"><img src="https://img.shields.io/static/v1?message=VK%20Chat&label=&color=blue"></a>
    <blockquote>VKBottle - это многофункциональный модуль для работы с VK Api и создания ботов</blockquote>
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
   pip install vkbottle==2.3
   ```

2) С помощью установщика pip из GitHub: 
   
   ```sh
   pip install https://github.com/timoniq/vkbottle/archive/master.zip --upgrade
   ```
   
### Кастомизация

<a href="https://github.com/Delgan/loguru"><img alt="downloads" src="https://img.shields.io/static/v1?label=powered%20by&message=loguru&color=orange"></a>
<a href="https://github.com/MagicStack/uvloop"><img alt="downloads" src="https://img.shields.io/static/v1?label=powered%20by&message=uvloop&color=purple"></a>

После установки `vkbottle` рекомендуется сразу же установить дополнительные модули `uvloop` и `loguru`, без них фреймворк работает медленне и логи не настраиваемы. О возможностях этих модулей можно прочитать в их документации

Установите `uvloop` и `loguru` с помощью команд:

```sh
pip install uvloop
pip install loguru
```

### Фишки

- Удобная и быстрая доставка сообщений через regex
- Быстрый API враппер
- Быстрый LongPoll фреймворк для ботов
- Маленький объем кода для достижения сложных конструкций
- Полностью асинхронно
- Множество встроенных помощников: Branches для цепей событий, [VBML](https://github.com/timoniq/vbml) для разметки сообщений и так далее
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
    return await bot.emulate(event=event, confirmation_token="ConfirmationToken")


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
from vkbottle.user import User
from vkbottle.user import types
from vkbottle.rule import VBMLUserRule

user = User("user-token", 123)
user.mode(2)

@user.on.message_new(VBMLUserRule("can i ask you about <theme>?",))
async def wrapper(ans: types.Message, theme):
    if theme in ["examples", "how to do smt", "depression", "insomnia"]:
        await ans("You can ask me about it in telegram @timoniq or make an issue on github!")
    else:
        await ans("Ok, sooner or later i ll respond you")

user.run_polling()
```

Больше примеров в папке [/examples](./examples)

### Документация

Полная документация:  

* [Русская версия документации](docs/README.RU.md)  
в ней же можно найти документацию по валидаторам, веткам

* [Дополнительная документация - русская версия](docs/FrameworkAPI.md)  
там можно найти все остальную информацию, уровень прочтения требует профессионального понимания фреймворка

# Contributing

ПР поддерживаются! Мне приятно видеть ваш вклад в развитие библиотеки  
Задавайте вопросы в блоке Issues и в чате VK!

## Лицензия

Copyright © 2019-2020 [timoniq](https://github.com/timoniq).  
Этот проект имеет [GPL-3.0](./LICENSE.txt) лицензию.
