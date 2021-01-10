from .dispatch.rules import user
from .framework.user import ABCUserLabeler, User, UserBlueprint, UserLabeler, user_run_multibot
from .tools.dev_tools.mini_types.user import MessageMin

Message = MessageMin
Blueprint = UserBlueprint
rules = user
