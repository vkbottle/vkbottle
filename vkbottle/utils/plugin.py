"""Read LICENSE.txt"""

"""
PLUGIN WRAPPER
"""


class Plugin:
    def __init__(self, bot, name='My Untitled Plugin', description=None, priority: int = 0):
        self.bot = bot
        self.name = name
        self.description = description
        # Decorators
        self.on = bot.on
