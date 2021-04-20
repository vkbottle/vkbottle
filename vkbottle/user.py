from .dispatch.rules import rules
from .framework.user import ABCUserLabeler, User, UserBlueprint, UserLabeler, run_multibot
from .tools.dev_tools.mini_types.user import MessageMin

Message = MessageMin
Blueprint = UserBlueprint
