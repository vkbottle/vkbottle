from vkbottle.tools.dev.mini_types.user import MessageMin

from . import base


class PeerRule(base.PeerRule[MessageMin]):
    pass


class CommandRule(base.CommandRule[MessageMin]):
    pass


class VBMLRule(base.VBMLRule[MessageMin]):
    pass


class RegexRule(base.RegexRule[MessageMin]):
    pass


class StickerRule(base.StickerRule[MessageMin]):
    pass


class FromPeerRule(base.FromPeerRule[MessageMin]):
    pass


class AttachmentTypeRule(base.AttachmentTypeRule[MessageMin]):
    pass


class ForwardMessagesRule(base.ForwardMessagesRule[MessageMin]):
    pass


class ReplyMessageRule(base.ReplyMessageRule[MessageMin]):
    pass


class GeoRule(base.GeoRule[MessageMin]):
    pass


class LevensteinRule(base.LevensteinRule[MessageMin]):
    pass


class MessageLengthRule(base.MessageLengthRule[MessageMin]):
    pass


class ChatActionRule(base.ChatActionRule[MessageMin]):
    pass


class PayloadRule(base.PayloadRule[MessageMin]):
    pass


class PayloadContainsRule(base.PayloadContainsRule[MessageMin]):
    pass


class PayloadMapRule(base.PayloadMapRule[MessageMin]):
    pass


class FromUserRule(base.FromUserRule[MessageMin]):
    pass


class FuncRule(base.FuncRule[MessageMin]):
    pass


class CoroutineRule(base.CoroutineRule[MessageMin]):
    pass


class StateRule(base.StateRule[MessageMin]):
    pass


class StateGroupRule(base.StateGroupRule[MessageMin]):
    pass


class MacroRule(base.MacroRule[MessageMin]):
    pass
