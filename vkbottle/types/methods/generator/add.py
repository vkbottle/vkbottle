from vkbottle.types.methods import *

listt = [
    Account,
    Ads,
    Appwidgets,
    Apps,
    Auth,
    Board,
    Database,
    Docs,
    Fave,
    Friends,
    Gifts,
    Groups,
    Leads,
    Likes,
    Market,
    Messages,
    Newsfeed,
    Notes,
    Notifications,
    Orders,
    Pages,
    Photos,
    Polls,
    Prettycards,
    Search,
    Secure,
    Stats,
    Status,
    Storage,
    Stories,
    Streaming,
    Users,
    Utils,
    Video,
    Wall,
    Widgets,
]
listt = [a.__name__ for a in listt]

for a in listt:
    print(f"self.{a.lower()} = {a}(self.request)")
