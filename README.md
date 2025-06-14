<p align="center">
  <a href="https://github.com/vkbottle/vkbottle">
    <img width="150px" height="150px" alt="VKBottle" src="https://raw.githubusercontent.com/vkbottle/vkbottle/master/docs/logo.svg">
  </a>
</p>
<h1 align="center">
  VKBottle
</h1>
<p align="center">
    <em><b>Кастомизируемый, быстрый и удобный фреймворк для работы с VK API</b></em>
</p>
<p align="center">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/vkbottle/vkbottle/push-build.yml">
  <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/vkbottle">
  <img alt="GitHub issues by-label" src="https://img.shields.io/github/issues/vkbottle/vkbottle/bug">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/vkbottle?color=green&label=PyPI">
</p>

## Hello World

```python
from vkbottle.bot import Bot

bot = Bot("GroupToken")

@bot.on.message()
async def handler(_) -> str:
    return "Hello, World!"

bot.run_forever()
```

[Смотреть больше примеров!](https://github.com/vkbottle/vkbottle/tree/master/examples)

## Документация

[Туториал для новичков](https://vkbottle.rtfd.io/ru/latest/tutorial/)\
[Техническая документация](https://vkbottle.rtfd.io/ru/latest)

## Установка

Установить новейшую версию можно командой:

```console
pip install vkbottle
```

Если вы ищете старые версии:

- [`3.x`](https://github.com/vkbottle/vkbottle/tree/v3.0)
- [`2.x`](https://github.com/vkbottle/vkbottle/tree/v2.0)

## Contributing

ПР поддерживаются! Перед созданием пулл реквеста ознакомьтесь с [CONTRIBUTION_GUIDE](CONTRIBUTION_GUIDE.md). Нам приятно видеть ваш вклад в развитие фреймворка.\
Задавайте вопросы в блоке Issues или на нашем [**форуме в Telegram**](https://t.me/botoforum)!

Мейнтейнеры: [click](https://github.com/vkbottle/vkbottle/graphs/contributors)

## Лицензия

Copyright © 2019 [timoniq](https://github.com/timoniq).\
Copyright © 2022-2024 [FeeeeK](https://github.com/FeeeeK).\
Copyright © 2024 [luwqz1](https://github.com/luwqz1).\
Этот проект имеет [MIT](https://github.com/vkbottle/vkbottle/blob/master/LICENSE) лицензию.
