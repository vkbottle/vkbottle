from vkbottle.framework.framework.handler import Handler


class Blueprint:
    def __init__(self, name: str = None, description: str = None):
        self.on: Handler = Handler()
        self.__name = name or "Unknown"
        self.__description = description or "Simple blueprint"

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name: str):
        self.__name = new_name

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, new_description: str):
        self.__description = new_description
