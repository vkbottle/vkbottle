# 

<h1 align="center">VKBottle - high quality VK Tool</h1>
<p align="center"><a href="https://pypi.org/project/vkbottle/"><img alt="downloads" src="https://img.shields.io/static/v1?label=pypi%20package&message=0.13&color=brightgreen"></a> <a href="https://github.com/timoniq/vkbottle"><img src="https://img.shields.io/static/v1?label=version&message=opensource&color=yellow" alt="service-test status"></a> <a href="https://vk.me/join/AJQ1d7fBUBM_800lhEe_AwJj"><img src="https://img.shields.io/static/v1?message=VK%20Chat&label=&color=blue"></a>
    <blockquote>VKBottle is high functional tool for creating VK Clients based on python</blockquote>
</p>
<hr>

### Install

1) From GitHub with git:
   
   ```sh
   git clone git://github.com/timoniq/vkbottler.git vkbottle
   ```

2) Now, install it to python site-packages if you don't want to use deployment import  
   You can use deployment import:
   
   ```python
   from .vkbottle.vkbottle import Bot
   ```
   You can install VKBottle to site-packages:
   ```sh
   cp vkbottler /path/to/python/site-packages
   ```

### Features

- Comfortable and fast regex message passing
- Fast API wrapper and requests
- Fast LongPoll Bot Framework
- You can use simple and minimalistic code to reach a big result
- Full VK Event Compatible
- Full Asyncio Support

***

### Longpoll

```python
from vkbottle import Bot, Message

bot = Bot('my-token', 123, debug=True)


@bot.on.message('My name is <name>')
async def wrapper(ans: Message, name):
    await ans('Hello, {}'.format(name))


if __name__ == '__main__':
    bot.run_polling()
```

### Callback

```python
from vkbottle import Bot, Message
from flask import request
# app = Flask()

bot = Bot('my-token', 123, debug=True)
confirmation = 'MyConfirmationCode'


@app.route('/')
def route():
    bot.process(event=request.args(), confirmation_token=confirmation)


@bot.on.message('My name is <name>')
async def wrapper(ans: Message, name):
    await ans('Hello, {}'.format(name))
```

More examples positioned in directory [/examples](./examples)

### Docs

Full docs you can find here:  

* [Russian Version](docs/README.RU.md)

# Contributing

Pull requests are welcome! I'm glad to see you work for our library  
Make issues if it is needed!

## License

Copyright © 2019 [timoniq](https://github.com/timoniq).  
This project is [GPL-3.0](./LICENSE.txt) licensed.
