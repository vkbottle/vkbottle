from vkbottle.tools.markdown_parser import StackFrame, Token, _handle_url


class TestHandleUrl:
    def test_url_open(self):
        stack = [StackFrame(None)]
        # 1. Open link
        _handle_url(Token("url_open", "["), stack)
        assert stack[-1].ctx_type == "url_text"

    def test_url_mid(self):
        stack = [StackFrame(None), StackFrame("url_text", open_marker="[")]
        # We write text into parts (simulating push)
        stack[-1].parts.append("VK")

        # 2. Close text, open href
        _handle_url(Token("url_mid", "]("), stack)
        assert stack[-1].ctx_type == "url_href"
        # url_data should be the text or Format object
        assert stack[-1].url_data is not None

    def test_url_close(self):
        stack = [StackFrame(None), StackFrame("url_href", url_data="VK")]
        stack[-1].parts.append("https://vk.com")

        # 3. Close href
        _handle_url(Token("url_close", ")"), stack)
        assert len(stack) == 1
        # Last part should be a url Format object
        from vkbottle.tools.formatting import Format

        last_part = stack[0].parts[-1]
        assert isinstance(last_part, Format)
        assert last_part.type == "url"

    def test_url_fallback_on_wrong_state(self):
        """If context is not url_text, url_mid should not change state."""
        stack = [StackFrame(None), StackFrame("bold", open_marker="**")]
        _handle_url(Token("url_mid", "]("), stack)
        # State should remain unchanged
        assert stack[-1].ctx_type == "bold"
