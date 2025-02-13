# UserAuth

Это простой инструмент для быстрого получения токена пользователя по логину и паролю.

!!! warning
    Мы не несем ответственности за блокировку ваших аккаунтов ([см. подробнее](../high-level/user.md))

```python
from vkbottle import UserAuth

login = "89012345678"
password = "qwerty123"

async def main():
    token = await UserAuth().get_token(login, password)
```

По умолчанию `UserAuth` использует для входа мобильное приложение вк.
Вы можете указать другое приложение, передав `client_id` и `client_secret` в конструктор `UserAuth`.

По умолчанию токен запрашивается с определенным списком прав доступа. Для переопределения этого списка можно в методе `get_token` использовать параметр `scope`. Список доступных прав перечислен ниже:

| Права                          | Описание                                                                                             | По умолчанию |
| ------------------------------ | ---------------------------------------------------------------------------------------------------- | ------------ |
| `UserPermission.notify`        | Пользователь разрешил отправлять ему уведомления                                                     | ✗            |
| `UserPermission.friends`       | Доступ к друзьям                                                                                     | ✓            |
| `UserPermission.photos`        | Доступ к фотографиям                                                                                 | ✓            |
| `UserPermission.audio`         | Доступ к аудиозаписям                                                                                | ✗            |
| `UserPermission.video`         | Доступ к видеозаписям                                                                                | ✓            |
| `UserPermission.stories`       | Доступ к историям                                                                                    | ✓            |
| `UserPermission.pages`         | Доступ к wiki-страницам                                                                              | ✓            |
| `UserPermission.menu`          | Добавление ссылки на приложение в меню слева                                                         | ✗            |
| `UserPermission.wallmenu`      | Быстрая публикация на стенах (устаревший параметр)                                                   | ✗            |
| `UserPermission.status`        | Доступ к статусу пользователя                                                                        | ✓            |
| `UserPermission.notes`         | Доступ к заметкам пользователя                                                                       | ✓            |
| `UserPermission.messages`      | Доступ к расширенным методам работы с сообщениями                                                    | ✗            |
| `UserPermission.wall`          | Доступ к обычным и расширенным методам работы со стеной                                              | ✓            |
| `UserPermission.ads`           | Доступ к расширенным методам работы с [рекламным API](https://dev.vk.com/ru/api/ads/getting-started) | ✓            |
| `UserPermission.offline`       | Доступ к API в любое время                                                                           | ✓            |
| `UserPermission.docs`          | Доступ к документам                                                                                  | ✓            |
| `UserPermission.groups`        | Доступ к группам пользователя                                                                        | ✓            |
| `UserPermission.notifications` | Доступ к оповещениям об ответах пользователю                                                         | ✓            |
| `UserPermission.stats`         | Доступ к статистике групп и приложений пользователя, администратором которых он является             | ✓            |
| `UserPermission.email`         | Доступ к email пользователя                                                                          | ✓            |
| `UserPermission.adsweb`        | Доступ к кабинету рекламной сети                                                                     | ✓            |
| `UserPermission.leads`         | Доступ к рекламным акциям                                                                            | ✗            |
| `UserPermission.exchange`      | Доступ к кабинету биржы рекламы                                                                      | ✓            |
| `UserPermission.market`        | Доступ к товарам                                                                                     | ✓            |
| `UserPermission.phone_number`  | Доступ к номеру телефона                                                                             | ✗            |

Пример получения токена с нужными правами:

```python
from vkbottle import UserAuth, UserPermission

login = "89012345678"
password = "qwerty123"

async def main():
    token = await UserAuth().get_token(login, password, scope=[UserPermission.photos, UserPermission.video])
```

При получении токена может потребоваться ввод капчи, либо дополнительное подтверждение через SMS или приложение для двухфакторной аутентификации (2FA). Ниже приведен пример с обработкой ошибок при получении токена:

```python
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, cast
from urllib.parse import parse_qs, urlparse

from vkbottle import APIAuthError, AuthError, CaptchaError, UserAuth

if TYPE_CHECKING:
    from typing import Optional, Union

login = "89012345678"
password = "qwerty123"

async def main():
    user_auth = UserAuth()

    auth_code: Union[bool, str] = True
    captcha_sid: Optional[str] = None
    captcha_key: Optional[str] = None

    while True:
        try:
            token = await user_auth.get_token(
                login,
                password,
                auth_code=auth_code,
                captcha_sid=captcha_sid,
                captcha_key=captcha_key
            )
            break
        except CaptchaError as error:
            captcha_sid = error.captcha_sid
            captcha_key = input(f"Open url '{error.captcha_img}' in browser and enter captcha code: ")
        except APIAuthError as error:
            if error.validation_type == "2fa_sms":
                validation_sid = cast(str, error.validation_sid)
                await user_auth.validate_phone(validation_sid)
                auth_code = input("Enter code from SMS: ")
                continue

            if error.validation_type == "2fa_app":
                print(f"Enter code from 2FA app here: {error.redirect_uri}")
                oauth_url = input("Enter OAuth URL from VK after signin in: ")
                parsed_url = urlparse(url=oauth_url)
                token = parse_qs(parsed_url.fragment)["access_token"][0]
                break

            print(error.error_description)
            return
        except AuthError as error:
            print(error.error_description)
            return

    print(f"Your token: {token}")

if __name__ == "__main__":
    asyncio.run(main())

```
