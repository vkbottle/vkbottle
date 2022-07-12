# API

Вы можете взаимодействовать с API ВКонтакте прямо из коробки.

```python
from vkbottle import API

# ...
api = API(token="token")
await api.messages.send(peer_id=1, message="Привет Павел Дуров!")
```

!!! warning "Внимание"
    Все методы в vkbottle пишутся *снейк_кейсом*. <br/>
    Это значит, например, что метод [`messages.getById`](https://dev.vk.com/method/messages.getById) в vkbottle пишется как `api.messages.get_by_id`.

## Параметры

* **token** - токен сообщества/пользователя или [генератор токенов](token-generator.md)
* **ignore_error** - игнорировать ошибки VK API
* **http_client** - клиент для запросов ([документация](../http/http-client.md))
* **request_rescheduler** - рещедулер запросов ([документация](request-rescheduler.md))

## Captcha хендлер

Должен решить капчу и вернуть ее код:

```python
from vkbottle import CaptchaError

bot = ...

async def captcha_handler(e: CaptchaError):
    ...
    return code

bot.api.add_captcha_handler(captcha_handler)
```
