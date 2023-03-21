from typing import TYPE_CHECKING

from vkbottle.modules import json

if TYPE_CHECKING:
    from .element import TemplateElement


def template_gen(*e: "TemplateElement"):
    """Generates dumped carousel out of box"""
    return json.dumps({"type": "carousel", "elements": [e.raw for e in e]})
