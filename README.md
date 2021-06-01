<p align="center">
  <a href="https://github.com/tesseradecade/vbml">
    <img src="https://github.com/timoniq/vkbottle/blob/master/docs/logo.jpg" width="200px" style="display: inline-block;">
  </a>
</p>
<h1 align="center">
  VKBottle 3.x
</h1>
<p align="center">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/timoniq/vkbottle/CI?style=flat-square">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/timoniq/vkbottle?style=flat-square">
  <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/timoniq/vkbottle/bug?style=flat-square">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/vkbottle?color=green&label=PyPI&style=flat-square">
</p>

> Кастомизируемый, быстрый и удобный фреймворк для работы с VK API

## Документация

[Туториал для новичков](https://github.com/timoniq/vkbottle/blob/master/docs/tutorial/index.md)\
[Техническая документация](https://vkbottle.readthedocs.io/ru/latest)

## Установка

Установить новейшую версию можно командой:

```shell
pip install -U https://github.com/timoniq/vkbottle/archive/master.zip
```

Установить версию 3.0 с PyPI можно командой:

```shell
pip install vkbottle
```

Если вы ищете старые версии (`2.x`) - [вам сюда](https://github.com/timoniq/vkbottle/tree/v2.0)

## Hello World

[Смотреть больше примеров!](https://github.com/timoniq/vkbottle/tree/master/examples)\
[Почему VKBottle?](https://github.com/timoniq/vkbottle/blob/master/docs/why_vkbottle.md)

```python
from vkbottle.bot import Bot

bot = Bot("GroupToken")

@bot.on.message()
async def handler(_) -> str:
    return "Hello world!"

bot.run_forever()
```

## Contributing

ПР поддерживаются! Перед созданием пулл реквеста ознакомьтесь с [CONTRIBUTION_GUIDE.md](CONTRIBUTION_GUIDE.md). Нам приятно видеть ваш вклад в развитие библиотеки. Задавайте вопросы в блоке Issues и в [**чате Telegram**](https://t.me/vkbottle_ru) / [**чате VK**](https://vk.me/join/AJQ1d7fBUBM_800lhEe_AwJj)!

## Лицензия

Copyright © 2019-2021 [timoniq](https://github.com/timoniq).\
Этот проект имеет [MIT](https://github.com/timoniq/vkbottle/blob/master/LICENSE) лицензию.
