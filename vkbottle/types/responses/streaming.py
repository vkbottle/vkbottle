from ..base import BaseModel


class GetServerUrl(BaseModel):
    endpoint: str = None
    key: str = None


class GetServerUrlModel(BaseModel):
    response: GetServerUrl = None
