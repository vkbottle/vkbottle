"""Read LICENSE.txt"""

"""
BOT MAIN API WRAPPER
"""

from .vkbottle import LongPollBot

from ..portable import API_VERSION

from ..vktypes.types.message import Message

from ..methods import Api

from .events import Events


Bot = LongPollBot
