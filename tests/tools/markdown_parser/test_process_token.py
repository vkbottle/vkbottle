from vkbottle.tools.markdown_parser import StackFrame, Token, _process_token


class TestProcessToken:
    def test_dispatch_to_format_bold(self):
        stack = [StackFrame(None)]
        token = Token(type="bold", value="**")
        _process_token(token, stack)
        assert stack[-1].ctx_type == "bold"

    def test_dispatch_to_format_italic(self):
        stack = [StackFrame(None)]
        token = Token(type="italic", value="*")
        _process_token(token, stack)
        assert stack[-1].ctx_type == "italic"

    def test_dispatch_to_underline_open(self):
        stack = [StackFrame(None)]
        token = Token(type="u_open", value="<u>")
        _process_token(token, stack)
        assert stack[-1].ctx_type == "u"

    def test_dispatch_to_underline_close(self):
        stack = [StackFrame(None), StackFrame("u", open_marker="<u>")]
        token = Token(type="u_close", value="</u>")
        _process_token(token, stack)
        assert len(stack) == 1  # Frame closed

    def test_dispatch_to_url_open(self):
        stack = [StackFrame(None)]
        token = Token(type="url_open", value="[")
        _process_token(token, stack)
        assert stack[-1].ctx_type == "url_text"

    def test_dispatch_to_literal(self):
        stack = [StackFrame(None)]
        token = Token(type="text", value="hello")
        _process_token(token, stack)
        assert "hello" in str(stack[-1].parts)

    def test_dispatch_to_escape(self):
        stack = [StackFrame(None)]
        token = Token(type="esc", value="\\*")
        _process_token(token, stack)
        assert "*" in str(stack[-1].parts)
