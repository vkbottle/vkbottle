from vkbottle.tools.markdown_parser import markdown


def test_markdown_preserves_stray_punctuation():
    # Stray <, >, ( and ) in ordinary text must survive, not be silently deleted.
    assert markdown("2 < 3 > 1") == "2 < 3 > 1"
    assert markdown("call foo(x) now") == "call foo(x) now"
    assert markdown("end ) here") == "end ) here"
