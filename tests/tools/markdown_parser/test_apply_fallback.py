from vkbottle.tools.markdown_parser import StackFrame, _apply_fallback


class TestApplyFallback:
    def test_unclosed_bold(self):
        """If ** is not closed, it becomes text."""
        stack = [StackFrame(None), StackFrame("bold", open_marker="**")]
        stack[-1].parts.append("text")

        _apply_fallback(stack)

        # In root frame parts there should be marker and text
        # Eg: '**' + 'text' or combined
        combined = "".join(str(p) for p in stack[0].parts)
        assert "**" in combined
        assert "text" in combined

    def test_unclosed_url_text(self):
        stack = [StackFrame(None), StackFrame("url_text", open_marker="[")]
        stack[-1].parts.append("text")

        _apply_fallback(stack)

        # Should become '[' + 'text' + ']('
        combined = "".join(str(p) for p in stack[0].parts)
        assert "[" in combined
        assert "text" in combined

    def test_unclosed_url_href(self):
        stack = [StackFrame(None), StackFrame("url_href", url_data="VK")]
        stack[-1].parts.append("https://vk.com")

        _apply_fallback(stack)

        # Should become '[VK](' + 'https://vk.com' + ')'
        combined = "".join(str(p) for p in stack[0].parts)
        assert "[VK]" in combined or "https://vk.com" in combined

    def test_no_fallback_needed(self):
        """If stack is already just root, do nothing."""
        stack = [StackFrame(None)]
        _apply_fallback(stack)
        assert len(stack) == 1
