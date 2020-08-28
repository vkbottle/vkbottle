# HTTP-Session-Manager

Сессиями клиентов распоряжается специальный менеджер

## Работа с менеджером сессий клиента

### http_client

Является типом http-клиента для создания сессии

### async with

```python
from vkbottle.http import SessionManager

# ...
session_manager = SessionManager()
async with session_manager as session:
    await session.request_text("https://google.com")
```

## Создание кастомного менеджера сессий клиента

Необходимо унаследоваться от `ABCSessionManager` и перегрузить `async with` методами `__aenter__` и `__aexit__`. Из первого необходимо вернуть клиента с открытой сессией, во втором эту сессию необходимо закрыть
