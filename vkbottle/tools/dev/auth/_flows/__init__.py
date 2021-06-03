"""
App authorization flows
vk.com/dev/access_token
"""

from .group import GroupAuthorizationCodeFlow, GroupImplicitFlow
from .service import ClientCredentialsFlow
from .user import UserAuthorizationCodeFlow, UserImplicitFlow
