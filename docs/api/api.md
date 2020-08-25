# API

Вы можете взаимодействовать с API ВКонтакте прямо из коробки.

```python
from vkbottle import API

api = API(token="token")
```

## Параметры

* **token** - токен сообщества/пользователя
* **ignore_error** - игнорировать ошибки VK API
* **session_manager** - менеджер сессий (читать документацию `http-session-manager`)
