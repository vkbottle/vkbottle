from vkbottle.tools.markdown_parser import _unescape


class TestUnescape:
    def test_basic_escape(self):
        assert _unescape(r"\*") == "*"
        assert _unescape(r"\_") == "_"
        assert _unescape(r"\[") == "["
        assert _unescape(r"\]") == "]"

    def test_no_escape(self):
        assert _unescape("plain text") == "plain text"
        assert _unescape("*bold*") == "*bold*"  # No backslash before markers

    def test_multiple_escapes(self):
        assert _unescape(r"\*bold\*") == "*bold*"

    def test_backslash_only(self):
        # Standalone backslash is not handled by the function's replace logic
        assert _unescape(r"\\") == "\\\\"
