from .events_list import EventList
from . import event

EVENT_DICT = {
    EventList.MESSAGE_NEW: event.MessageNew,
    EventList.MESSAGE_REPLY: event.MessageReply,
    EventList.MESSAGE_EDIT: event.MessageEdit,
    EventList.MESSAGE_ALLOW: event.MessageAllow,
    EventList.MESSAGE_DENY: event.MessageDeny,

    EventList.PHOTO_NEW: event.PhotoNew,
    EventList.PHOTO_COMMENT_NEW: event.PhotoCommentNew,
    EventList.PHOTO_COMMENT_EDIT: event.PhotoCommentEdit,
    EventList.PHOTO_COMMENT_RESTORE: event.PhotoCommentRestore,
    EventList.PHOTO_COMMENT_DELETE: event.PhotoCommentDelete,

    EventList.AUDIO_NEW: event.AudioNew,

    EventList.VIDEO_NEW: event.VideoNew,
    EventList.VIDEO_COMMENT_NEW: event.VideoCommentNew,
    EventList.VIDEO_COMMENT_EDIT: event.VideoCommentEdit,
    EventList.VIDEO_COMMENT_RESTORE: event.VideoCommentRestore,
    EventList.VIDEO_COMMENT_DELETE: event.VideoCommentDelete,

    EventList.WALL_POST_NEW: event.WallPostNew,
    EventList.WALL_REPOST: event.WallRepost,
    EventList.WALL_REPLY_NEW: event.WallReplyNew,
    EventList.WALL_REPLY_EDIT: event.WallReplyEdit,
    EventList.WALL_REPLY_RESTORE: event.WallReplyRestore,
    EventList.WALL_REPLY_DELETE: event.WallReplyDelete,

    EventList.BOARD_POST_NEW: event.BoardPostNew,
    EventList.BOARD_POST_EDIT: event.BoardPostEdit,
    EventList.BOARD_POST_RESTORE: event.BoardPostRestore,
    EventList.BOARD_POST_DELETE: event.BoardPostDelete,

    EventList.MARKET_COMMENT_NEW: event.MarketCommentNew,
    EventList.MARKET_COMMENT_EDIT: event.MarketCommentEdit,
    EventList.MARKET_COMMENT_RESTORE: event.MarketCommentRestore,
    EventList.MARKET_COMMENT_DELETE: event.MarketCommentDelete,

    EventList.GROUP_LEAVE: event.GroupLeave,
    EventList.GROUP_JOIN: event.GroupJoin,
    EventList.USER_BLOCK: event.UserBlock,
    EventList.USER_UNBLOCK: event.UserUnblock,

    EventList.POLL_VOTE_NEW: event.PollVoteNew,
    EventList.GROUP_OFFICERS_EDIT: event.GroupOfficersEdit,
    EventList.GROUP_CHANGE_SETTINGS: event.GroupChangeSettings,
    EventList.GROUP_CHANGE_PHOTO: event.GroupChangePhoto
}
