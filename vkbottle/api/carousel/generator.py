from vkbottle.utils import json
from .element import CarouselEl


def carousel_gen(*e: CarouselEl):
    """ Generates dumped carousel out of box """
    return json.dumps({"type": "carousel", "elements": [e.raw for e in e]})
