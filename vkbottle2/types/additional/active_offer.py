from ..base import BaseModel

# returned from https://vk.com/dev/account.getActiveOffers


class ActiveOffer(BaseModel):
    id: str = None
    title: str = None
    instruction: str = None
    instruction_html: str = None
    short_description: str = None
    description: str = None
    img: str = None
    tag: str = None
    price: int = None
