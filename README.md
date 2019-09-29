# What is VKBottle
[![PyPI](https://badge.fury.io/py/vkbottle.svg)](https://pypi.org/project/vkbottle/) 
[![VK Chat](https://img.shields.io/badge/Vk-Chat-blue)](https://vk.me/join/AJQ1d7fBUBM_800lhEe_AwJj) 
[![Build Status](https://travis-ci.com/timoniq/vkbottle.svg?branch=master)](https://travis-ci.com/timoniq/vkbottle)

### Install

From GitHub:

```sh
pip install https://github.com/timoniq/vkbottle/archive/master.zip --upgrade
```

From PyPI (old release):

```sh
pip install vkbottle
```

### Features

- Comfortable and fast regex message passing
- Fast API wrapper and requests
- Fast LongPoll Bot Framework
- You can use simple and minimalistic code to reach a big result
- Full VK Event Compatible
- Full Asyncio Support

### Usage

```python
from vkbottle import Bot, Message

bot = Bot('my-token', 123, debug=True)


@bot.on.message('My name is <name>')
async def wrapper(ans: Message, name):
    await ans('Hello, {}'.format(name))
   
   
if __name__ == '__main__':
    bot.run()
```

More examples positioned in directory [/examples](./examples)

### Docs

Full docs you can find here:  
* [Russian Version](./docs/readme.ru.md)
* [English Version](./docs/kriper2005.txt)

# Contributing

Pull requests are welcome! I'm glad to see you work for our library  
Make issues if it is needed!

## License

Copyright © 2019 [timoniq](https://github.com/timoniq).  
This project is [MIT](./LICENSE.txt) licensed.
