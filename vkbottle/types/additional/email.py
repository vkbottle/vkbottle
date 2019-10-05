from ..base import BaseModel

# returned from https://vk.com/dev/messages.getChatPreview?params[peer_id]=123&params[v]=5.101


class Email(BaseModel):
    id: int = None
    address: str = None
