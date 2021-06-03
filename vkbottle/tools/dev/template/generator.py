from vkbottle.modules import json

from .element import TemplateElement


def template_gen(*e: TemplateElement):
    """Generates dumped carousel out of box"""
    return json.dumps({"type": "carousel", "elements": [e.raw for e in e]})
