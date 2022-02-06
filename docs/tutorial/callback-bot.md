# Подключение CallbackAPI

> ⚠️ Обязательно к прочтению: https://dev.vk.com/api/callback/getting-started

> ⚠️ У вас должен иметься собственный сервер с доменным именем. DDNS работать не будет. Также подразумевается наличие опыта в настройке веб-серверов.

Для подключения `CallbackAPI` к вашему сообществу:

1. Инициализировать параметры для настройки, например, таким образом:
    ```python
    import os
    TOKEN = os.getenv("VK_TOKEN") # ключ сообщества
    url = os.getenv("VK_URL") # url = "http://example.com/whateveryouwnant"
    title = os.getenv("VK_TITLE") # title = "server"
    secret_key = os.getenv("VK_SECRET_KEY") # опционально
    ```
2. Импортировать `BotCallback` из `vkbottle.callback` и указать параметры для настройки:
    ```python
    from vkbottle.callback import BotCallback
    callback = BotCallback(
        url = url,
        title = title
    )
    ```
3. Инициализировать бота:
    ```python
    from vkbottle import Bot
    bot = Bot(token=TOKEN, callback=callback)
    ```

4. Настроить любой сервер (`aiohttp`, `flask`, `fastapi`) и обрабатывать полученные события. Для более полного ознакомления рекомендуется посмотреть пример.
    ```python
    # event - событие, полученное от vk
    await bot.process_event(event)
    ```

    > ⚠️ После подключения бот получит только запрос с подтверждением, для получения остальных событий необходимо включить их в настройках группы.

## Пример

<!-- Необходимо будет вставить ссылку на пример с репозиторием из vkbottle -->

* [Подключение CallbackAPI](link)