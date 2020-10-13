from pydantic import BaseModel
from typing import List


class UserCodeFlowResponse(BaseModel):
    access_token: str
    expires_in: int
    user_id: int


class GroupCodeFlowResponse(BaseModel):
    """
    Ignoring access_token_XXXXXX keys
    Unable to parse them with pydantic and they are already in 'groups'
    Documentation: vk.com/dev/authcode_flow_group
    """

    class Group(BaseModel):
        group_id: int
        access_token: str

    groups: List[Group]
    expires_in: int


class CredentialsFlowResponse(BaseModel):
    access_token: str
