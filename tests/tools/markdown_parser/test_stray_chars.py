from vkbottle.tools.markdown_parser import markdown


def test_markdown_preserves_stray_punctuation():
    # Stray <, >, ( and ) in ordinary text must survive, not be silently deleted.
    assert markdown("2 < 3 > 1") == "2 < 3 > 1"
    assert markdown("call foo(x) now") == "call foo(x) now"
    assert markdown("end ) here") == "end ) here"


def test_markdown_orphan_close_underline_is_literal():
    # An orphan </u> must render as </u>, not collapse to <u> (slash dropped).
    assert markdown("hello </u> world") == "hello </u> world"


def test_markdown_unclosed_link_does_not_fabricate_paren():
    # An unclosed [text](href must not gain a trailing ) the user never typed.
    assert markdown("see [text](http://x") == "see [text](http://x"


def test_markdown_link_href_is_literal():
    # Markup characters inside a link target must be kept literally, not parsed as
    # formatting (which would strip them and corrupt the URL).
    result = markdown("[text](http://x*y*z)")

    assert result.type == "url"
    assert result.data["url"] == "http://x*y*z"
    assert result.string == "text"
