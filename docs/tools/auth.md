# Authorization Flows

Authorization Flows являются набором классов для удобной работы с получением ключа доступа `VK API`

Всего есть 3 вида путей получения ключа доступа:

1. Implicit flow

2. Authorization code flow

3. Client credentials flow

Подробнее про каждый вы можете прочитать в [документации](https://vk.com/dev/access_token)

## auth_dialog_link

Cвойство, которое возвращает ссылку на окно авторизации

## parse_scope(scope: Optional\[Union\[int, List\[int\]\]\]) -> Optional\[int\]:

Метод для удобной обработки `scope`

## ABCImplicitFlow

Абстрактный класс для `ImplicitFlow`  
Не добавляет функционала, нужен только для семантики

## ABCAuthorizationCodeFlow

Абстрактный класс для `AuthorizationCodeFlow`

### get_model()

Геттер модели со схемой, которая обработает ответ с токеном

### get_token_request_link(client_secret: str, code: str) -> str

Геттер ссылки на запрос получение токена

### request_token(client_secret: str, code: str)

Запрос на получение токена из кода и возврат соответстующей модели