"""
App authorization flows
vk.com/dev/access_token
"""

from .group import GroupImplicitFlow, GroupAuthorizationCodeFlow
from .service import ClientCredentialsFlow
from .user import UserImplicitFlow, UserAuthorizationCodeFlow
