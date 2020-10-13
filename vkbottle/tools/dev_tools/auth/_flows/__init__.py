"""
App authorization flows
vk.com/dev/access_token
"""

from .user import UserImplicitFlow, UserAuthorizationCodeFlow
from .group import GroupImplicitFlow, GroupAuthorizationCodeFlow
from .service import ClientCredentialsFlow
