from vkbottle.framework.labeler import BotLabeler


def test_vbml_ignore_case_getter_reads_real_key():
    labeler = BotLabeler()
    # The getter must read the real 'vbml_flags' key, not a non-existent 'flags' key.
    assert labeler.vbml_ignore_case is False

    labeler.vbml_ignore_case = True
    assert labeler.vbml_ignore_case is True
