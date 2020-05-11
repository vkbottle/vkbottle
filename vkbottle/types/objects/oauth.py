from ..base import BaseModel


class Error(BaseModel):
    error: str = None
    error_description: str = None
    redirect_uri: str = None


Error.update_forward_refs()
