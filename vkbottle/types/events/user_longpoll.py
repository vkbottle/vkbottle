from enum import IntEnum


class UserEvents(IntEnum):
    replace_message_flags = 1
    install_message_flags = 2
    reset_message_flags = 3
    new_message = 4
    edit_message = 5
    in_read = 6
    out_read = 7
    friend_online = 8
    friend_offline = 9
    reset_dialog_flags = 10
    replace_dialog_flags = 11
    install_dialog_flags = 12
    delete_messages = 13
    chat_restore = 14

    topic_params_change = 51
    chat_info_edit = 52
    dialog_typing_state = 61
    conversation_typing_state = 62
    chat_voice_message_states = 64
    call = 70
    counter = 80
    notifications_settings_changed = 114
