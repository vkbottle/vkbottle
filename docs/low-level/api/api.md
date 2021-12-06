# API

Вы можете взаимодействовать с API ВКонтакте прямо из коробки.

```python
from vkbottle import API

api = API(token="token")
```

## Параметры

* **token** - токен сообщества/пользователя или [генератор токенов](token-generator.md)
* **ignore_error** - игнорировать ошибки VK API
* **http_client** - клиент для запросов ([документация](../http/http-client.md))
* **request_rescheduler** - рещедулер запросов ([документация](request-rescheduler.md))
