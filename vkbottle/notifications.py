"""Read LICENSE.txt"""

from .project_collections import colored


plugin_folder = 'Plugin Folder was created, PATH "{}"'

newer_version = 'Newer version of VKBottle available ({})! ' \
                'Install it using ' + colored('pip install vkbottle --upgrade', 'yellow')

newest_version = 'You are using the newest version of VKBottle'

bot_auth = 'Bot <' + colored('{}', 'magenta') + '> was authorised successfully'

module_longpoll = 'MODULE USING LONGPOLL VERSION {}'

deprecated_name = 'Name \'{}\' is now deprecated. Use name \'{}\' and read the docs'

messages_decorators = 'Found {} message decorators'

longpoll_connection_error = 'LongPoll Connection error! Check your internet connection and try again!'

longpoll_not_enabled = 'LongPoll is not enabled in your group'

request_connection_timeout = 'Request Connect Timeout! Reloading..'

runtime_error = 'ATTENTION! Warn ({}) is called often because you use async ' \
                'functions when \'async_use\' is False or upside down!'

add_undefined = colored('Add to your on-message file an on-message-undefined decorator', 'yellow')

keyboard_interrupt = colored('VKBottle successfully stopped by Keyboard Interrupt', 'yellow')
