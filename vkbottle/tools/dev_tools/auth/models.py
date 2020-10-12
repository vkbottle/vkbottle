from pydantic import BaseModel


class UserCodeFlowResponse(BaseModel):
    access_token: str
    expires_in: int
    user_id: int
