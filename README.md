<p align="center">
  <a href="https://github.com/vkbottle/vkbottle">
    <img src="https://raw.githubusercontent.com/vkbottle/vkbottle/master/docs/logo.svg" width="175px" style="display: inline-block; border-radius: 5px">
  </a>
</p>
<h1 align="center">
  VKBottle 4.x
</h1>
<p align="center">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/vkbottle/vkbottle/CI?style=flat-square">
  <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/vkbottle/vkbottle?style=flat-square">
  <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/vkbottle/vkbottle/bug?style=flat-square">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/vkbottle?color=green&label=PyPI&style=flat-square">
</p>

> Кастомизируемый, быстрый и удобный фреймворк для работы с VK API

## Документация

[Туториал для новичков](https://vkbottle.readthedocs.io/ru/latest/tutorial/)\
[Техническая документация](https://vkbottle.readthedocs.io/ru/latest)

## Установка

Установить новейшую версию можно командой:

```shell
pip install -U https://github.com/vkbottle/vkbottle/archive/master.zip
```

Установить последнюю версию VKBottle 4.x с PyPI можно командой:

```shell
pip install vkbottle
```

Если вы ищете старые версии:
- [`3.x`](https://github.com/vkbottle/vkbottle/tree/v3.0)
- [`2.x`](https://github.com/vkbottle/vkbottle/tree/v2.0)

## Hello World

[Смотреть больше примеров!](https://github.com/vkbottle/vkbottle/tree/master/examples)\
[Почему VKBottle?](https://github.com/vkbottle/vkbottle/blob/master/docs/why_vkbottle.md)

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

* Создатель [@timoniq](https://github.com/timoniq)
* Мейнтейнер [@FeeeeK](https://github.com/FeeeeK)

## Лицензия

Copyright © 2019-2021 [timoniq](https://github.com/timoniq).\
Copyright © 2022 [FeeeeK](https://github.com/FeeeeK).\
Этот проект имеет [MIT](https://github.com/vkbottle/vkbottle/blob/master/LICENSE) лицензию.
