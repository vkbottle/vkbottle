from vkbottle.tools.formatting import Format, bold
from vkbottle.tools.markdown_parser import _join


class TestJoin:
    def test_join_strings(self):
        res = _join(["hello ", "world"])
        assert res == "hello world"
        assert isinstance(res, str)

    def test_join_format(self):
        # Simulate that parts contain Format
        res = _join(["hello ", bold("world")])
        # Result should be Format, since bold("world") is Format
        assert isinstance(res, Format)
        assert str(res) == "hello world"

    def test_empty_list(self):
        assert _join([]) == ""

    def test_join_multiple_formats(self):
        res = _join([bold("a"), " and ", bold("b")])
        assert isinstance(res, Format)
        assert str(res) == "a and b"
