import types

from vkbottle.framework.bot import multibot
from vkbottle.polling import BotPolling


def _run_multibot(mocker, *, skip_old_events=True):
    recorded = []

    def polling_factory():
        polling = BotPolling()
        recorded.append(polling)
        return polling

    class _Bot:
        error_handler = object()

        def __init__(self):
            self.skip_old_events = skip_old_events
            self.startup_tasks: list = []
            self.on_startup: list = []
            self.on_shutdown: list = []

        def run_polling(self, custom_polling):
            return None

    mocker.patch.object(multibot, "_run")
    mocker.patch.object(multibot, "SingleAiohttpClient")

    bot = _Bot()
    apis = [types.SimpleNamespace(http_client=None)]
    multibot.run_multibot(bot, apis, polling_type=polling_factory)
    return bot, recorded[0]


def test_run_multibot_propagates_error_handler(mocker):
    bot, polling = _run_multibot(mocker)
    # Each per-API polling must use the bot's error handler, not its own default.
    assert polling.error_handler is bot.error_handler
