from .dispatch.rules import user as rules
from .dispatch.views import user as views
from .framework.user import ABCUserLabeler, User, UserBlueprint, UserLabeler, run_multibot
from .tools.dev_tools.mini_types.bot import MessageMin

Message = MessageMin
Blueprint = UserBlueprint
