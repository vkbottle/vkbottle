# Bot

Инстанс бота состоит из стандартного апи, лонгпола и других частей фреймворка.

Атрибуты:

`bot.api` - [API документация](../low-level/api.md)<br/>
`bot.router` - [Router документация](../high-level/handling/router.md)<br/>
`bot.labeler`/`bot.on` - [Labeler документация](bot/labeler.md)<br/>
`bot.polling` - [Polling документация](../low-level/polling.md)<br/>
`bot.callback` - [Callback документация](../low-level/callback.md)<br/>
`bot.error_handler` - [Error handler документация](../low-level/exception_handling/error-handler.md)<br/>
`bot.loop_wrapper` - [Loop Wrapper документация](../tools/loop-wrapper.md)<br/>

Функции:

## Long Poll API

### `bot.run_polling()`

Асинхронный запуск longpoll

### `bot.run()`

Синхронный запуск longpoll. Добавляет `run_polling` в таски `bot.loop_wrapper` и вызывает `bot.loop_wrapper.run()`

## Callback API

### `bot.setup_webhook()`

Устанавливает сервер для `CallbackAPI` в сообщество

### `bot.process_event(event)`

Передает полученное событие в роутер, для его обработки

## Dual mode

Long Poll и Callback API могут работать одновременно: запустите Long Poll через
`bot.run()` (или `await bot.run_polling()`), а события HTTP-сервера, как обычно,
передавайте в `await bot.process_event(event)`. Чтобы обработать одно событие только
один раз, создайте бота с `dual_mode=True`:

```python
bot = Bot(token=TOKEN, callback=callback, dual_mode=True)
```

В этом режиме бот атомарно запоминает событие в локальном TTL-кэше до его передачи
в роутер. По умолчанию запись хранится 300 секунд, а кэш содержит до 10 000 ключей;
параметры можно изменить через `event_deduplication_ttl` и
`event_deduplication_cache_size`. Кэш хранится в памяти процесса, поэтому для
нескольких процессов нужен общий внешний механизм дедупликации.
