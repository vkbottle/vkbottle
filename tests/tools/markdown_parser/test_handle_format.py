from vkbottle.tools.markdown_parser import StackFrame, Token, _handle_format


class TestHandleFormat:
    def test_open_bold(self):
        stack = [StackFrame(ctx_type=None)]
        token = Token(type="bold", value="**")
        _handle_format(token, stack)
        assert len(stack) == 2
        assert stack[-1].ctx_type == "bold"
        assert stack[-1].open_marker == "**"

    def test_close_bold(self):
        stack = [StackFrame(None), StackFrame("bold", open_marker="**")]
        token = Token(type="bold", value="**")
        _handle_format(token, stack)
        assert len(stack) == 1  # Frame closed

    def test_open_italic(self):
        stack = [StackFrame(ctx_type=None)]
        token = Token(type="italic", value="*")
        _handle_format(token, stack)
        assert stack[-1].ctx_type == "italic"

    def test_close_italic(self):
        stack = [StackFrame(None), StackFrame("italic", open_marker="*")]
        token = Token(type="italic", value="*")
        _handle_format(token, stack)
        assert len(stack) == 1
