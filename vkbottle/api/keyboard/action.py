from ...utils import except_none_self
from vkbottle.utils.exceptions import KeyboardError


class Action:
    def __init__(
        cls,
        label: str = None,
        payload: str = None,
        link: str = None,
        hash: str = None,
        app_id: int = None,
        owner_id: int = None,
    ):
        for k, v in except_none_self(locals()).items():
            if not hasattr(cls, k):
                raise KeyboardError(
                    "Action {} cannot assign {}".format(cls.__class__.__name__, k)
                )
            setattr(cls, k, v)
        cls.type = getattr(cls, "type")

    def dict(self):
        return vars(self)

    def __repr__(self):
        return f"<Keyboard (action) {self.__class__.__qualname__}>"


class Text(Action):
    type = "text"
    label = None
    payload = None


class OpenLink(Action):
    type = "open_link"
    link: str = None
    label: str = None
    payload: str = None


class Location(Action):
    type = "location"
    payload: str = None


class VKPay(Action):
    type = "vkpay"
    payload: str = None
    hash: str = None


class VKApps(Action):
    type = "open_app"
    app_id: int = None
    owner_id: int = None
    payload: str = None
    label: str = None
    hash: str = None
