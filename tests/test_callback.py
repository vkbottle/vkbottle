import secrets

from vkbottle.callback import bot_callback
from vkbottle.callback.bot_callback import BotCallback


def test_callback_secret_key_uses_secrets_and_rich_alphabet():
    # The callback secret_key authenticates VK callbacks, so it must come from the
    # cryptographic `secrets` module, not the predictable `random` PRNG.
    assert bot_callback.choice is secrets.choice

    assert len(BotCallback().secret_key) == 32
    # Keys are richer than lowercase-only (statistically certain across samples).
    many = "".join(BotCallback().secret_key for _ in range(5))
    assert any(c.isupper() or c.isdigit() for c in many)
