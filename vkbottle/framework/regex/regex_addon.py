import re


class RegexHelper(object):
    group_id: int

    def init_bot_mention(self, text):
        pattern = r'^\[club' + str(self.group_id) + r'\|[@a-zA-Z0-9.]+\] '
        return re.sub(pattern, '', text)
