import os


class WhiteList(object):
    plugin_folder: str
    use_whitelist: bool
    whitelist: list

    def whitelist_initialise(self):
        whitelist_path = self.plugin_folder + "/whitelist.txt"

        if not os.path.isfile(whitelist_path):
            open(whitelist_path, "a").close()

        with open(whitelist_path, "r+") as whitelist_doc:
            if self.whitelist != list():
                for string in self.whitelist:
                    whitelist_doc.write(str(string) + "\n")
            else:
                self.whitelist = [
                    int(line) for line in whitelist_doc.read().splitlines()
                ]

        self.use_whitelist = True

    def __update_whitelist_doc(self):
        if self.use_whitelist:
            whitelist_path = self.plugin_folder + "/whitelist.txt"
            with open(whitelist_path, "w") as f:
                for string in self.whitelist:
                    f.write(str(string) + "\n")

    async def add_whitelist(self, *user_id: int):
        if self.use_whitelist:
            self.whitelist.extend(user_id)
            self.__update_whitelist_doc()

    async def remove_from_whitelist(self, *user_ids: int):
        if self.use_whitelist:
            for user_id in user_ids:
                if user_id in self.whitelist:
                    self.whitelist.pop(self.whitelist.index(user_id))
            self.__update_whitelist_doc()
        return self.whitelist

    async def check_for_whitelist(self, obj: dict):
        peer_id = obj.get("from_id", 0)
        return self.use_whitelist is False or peer_id in self.whitelist
