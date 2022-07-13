# UserAuth

Это простой инструмент для быстрого получения токена пользователя по логину и паролю.

```python
from vkbottle import UserAuth

login = "89012345678"
password = "qwerty123"

async def main():
    token = await UserAuth().get_token(login, password)
```

По умолчанию `UserAuth` использует для входа мобильное приложение вк.
Вы можете указать другое приложение, передав `client_id` и `client_secret` в конструктор `UserAuth`.

!!! warning
    Мы не несем ответственности за блокировку ваших аккаунтов. [Подробнее](../high-level/user/user.md)
