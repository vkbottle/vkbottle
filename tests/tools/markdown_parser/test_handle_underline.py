from vkbottle.tools.markdown_parser import StackFrame, Token, _handle_underline


class TestHandleUnderline:
    def test_open_u(self):
        stack = [StackFrame(None)]
        token = Token(type="u_open", value="<u>")
        _handle_underline(token, stack)
        assert stack[-1].ctx_type == "u"

    def test_close_u(self):
        stack = [StackFrame(None), StackFrame("u", open_marker="<u>")]
        token = Token(type="u_close", value="</u>")
        _handle_underline(token, stack)
        assert len(stack) == 1

    def test_ignore_non_u_context(self):
        """u_open always opens a new 'u' frame regardless of current context."""
        stack = [StackFrame(None), StackFrame("bold", open_marker="**")]
        token = Token(type="u_open", value="<u>")
        _handle_underline(token, stack)
        assert stack[-1].ctx_type == "u"
        assert stack[-1].open_marker == "<u>"
