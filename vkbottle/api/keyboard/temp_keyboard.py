import json


class KeyboardError(Exception):
    pass


class TextButton:

    def __init__(self, label, payload: dict = None, color=None):
        self.type = 'text'
        self.color = color or 'default'
        self.label = label
        self.payload = payload or {}


class OpenLinkButton:

    def __init__(self, label, link, payload: dict = None, color=None):
        self.type = 'open_link'
        self.color = color or 'default'
        self.label = label
        self.link = link
        self.payload = payload or {}


class LocationButton:

    def __init__(self, payload: dict = None, color=None):
        self.type = 'location'
        self.color = color or 'default'
        self.payload = payload or {}


class VkPayButton:

    def __init__(self, label, app_id, owner_id, hash=None, payload: dict = None, color=None):
        self.type = 'vkpay'
        self.color = color or 'default'
        self.label = label
        self.app_id = app_id
        self.owner_id = owner_id
        self.hash = hash
        self.payload = payload or {}


class VkAppsButton:

    def __init__(self, label, payload: dict = None, color=None):
        self.type = 'open_app'
        self.color = color or 'default'
        self.label = label
        self.payload = payload or {}


class CallbackButton:

    def __init__(self, label, payload: dict = None, color=None):
        self.type = 'callback'
        self.color = color or 'default'
        self.label = label
        self.payload = payload or {}


class Keyboard:

    def __init__(self, one_time=False, inline=False):
        self.buttons = []
        self.one_time = one_time
        self.inline = inline

    def add_row(self):
        if len(self.buttons) and not len(self.buttons[-1]):
            raise KeyboardError('Last row is empty!')
        self.buttons.append([])
        return self

    def add_button(self, *btns):
        if len(btns) > 5:
            raise KeyboardError('Exceeded the maximum size: "5 × 10" or "5 × 6"')
        self.buttons[-1].extend(btns)
        return self

    def create(self):
        buttons = []
        for row in self.buttons:
            rows = []
            for btn in row:
                action = dict(btn.__dict__)
                action.pop('color')
                rows.append({'action': action, 'color': btn.color})
            buttons.append(rows)

        keyboard = {
            'one_time': self.one_time,
            'inline': self.inline,
            'buttons': buttons
        }
        return json.dumps(keyboard)

    def __str__(self):
        return self.create()

    def __repr__(self):
        return f"<Keyboard (generator) {len(self.buttons)} buttons>"
