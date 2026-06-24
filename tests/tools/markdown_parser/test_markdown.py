from vkbottle.tools.formatting import Format
from vkbottle.tools.markdown_parser import markdown


def test_plain_no_change():
    res = markdown("plain text")
    assert isinstance(res, str)
    assert res == "plain text"


def test_bold_inline():
    res = markdown("plain **bold** text")
    assert isinstance(res, Format)
    data = res.as_data()
    assert any(item.get("type") == "bold" for item in data.get("items", []))
    assert str(res) == "plain bold text"


def test_italic_inline():
    res = markdown("plain *italic* text")
    assert isinstance(res, Format)
    data = res.as_data()
    assert any(item.get("type") == "italic" for item in data.get("items", []))
    assert str(res) == "plain italic text"


def test_underline_html():
    res = markdown("plain <u>underline</u> text")
    assert isinstance(res, Format)
    data = res.as_data()
    assert any(item.get("type") == "underline" for item in data.get("items", []))
    assert str(res) == "plain underline text"


def test_url_link():
    res = markdown("Check [VK](https://vk.com)")
    assert isinstance(res, Format)
    data = res.as_data()
    assert any(item.get("type") == "url" for item in data.get("items", []))
    assert "VK" in str(res)


def test_escaping_literal_star():
    res = markdown("\\*not-italic*")
    assert isinstance(res, str)
    assert res == "*not-italic*"


def test_bold_contains_italic():
    """**bold *italic* text** — italic inside bold"""
    res = markdown("**bold *italic* text**")
    assert isinstance(res, Format)
    data = res.as_data()
    # Check that both bold and italic exist
    types = [item.get("type") for item in data.get("items", [])]
    assert "bold" in types
    assert "italic" in types
    assert str(res) == "bold italic text"


def test_italic_contains_bold():
    """*italic **bold** text* — bold inside italic"""
    res = markdown("*italic **bold** text*")
    assert isinstance(res, Format)
    data = res.as_data()
    types = [item.get("type") for item in data.get("items", [])]
    assert "italic" in types
    assert "bold" in types
    assert str(res) == "italic bold text"


def test_triple_closes_nested():
    res = markdown("plain **bold *nested***")
    assert isinstance(res, Format)
    assert str(res) == "plain bold nested"

    data = res.as_data()
    items = data.get("items", [])

    # Check presence of both formats
    types = {item["type"] for item in items}
    assert "bold" in types
    assert "italic" in types

    # Optional: verify they overlap (sign of nesting in VK API)
    bold_item = next(i for i in items if i["type"] == "bold")
    italic_item = next(i for i in items if i["type"] == "italic")

    # italic should start inside bold and end together with it or earlier
    bold_start = bold_item["offset"]
    bold_end = bold_start + bold_item["length"]
    italic_start = italic_item["offset"]
    italic_end = italic_start + italic_item["length"]

    assert italic_start >= bold_start  # italic inside bold
    assert italic_end <= bold_end  # italic does not go beyond bold


def test_multiple_nested_levels():
    """**a *b **c*** d** — symmetric complex nesting"""
    res = markdown("**a *b **c*** d**")
    assert isinstance(res, Format)
    assert str(res) == "a b c d"

    data = res.as_data()
    items = data.get("items", [])

    types = {item["type"] for item in items}
    assert "bold" in types
    assert "italic" in types


def test_adjacent_formats_not_nested():
    """**bold***italic* — adjacent, but not nested formats"""
    res = markdown("**bold***italic*")
    assert isinstance(res, Format)
    assert str(res) == "bolditalic"

    data = res.as_data()
    types = [item.get("type") for item in data.get("items", [])]
    # Should be both formats on the same level
    assert types.count("bold") == 1
    assert types.count("italic") == 1

    res = markdown("*italic***bold**")
    assert isinstance(res, Format)
    assert str(res) == "italicbold"

    data = res.as_data()
    types = [item.get("type") for item in data.get("items", [])]
    # Should be both formats on the same level
    assert types.count("bold") == 1
    assert types.count("italic") == 1


# === NEW TESTS: Escaping ===


def test_escape_outer_not_inner():
    r"""\**not-bold* but *italic* inside** — escaped outer, inner works"""
    res = markdown("\\**not-bold* but *italic* inside**")

    # \* escapes only the first star. Remaining markers form valid pairs *...*
    # Therefore formatting applies, but bold does NOT open
    assert isinstance(res, Format)
    data = res.as_data()
    types = {item.get("type") for item in data.get("items", [])}

    assert "bold" not in types, "Bold should not open due to escaping the first marker"
    assert "italic" in types, "Italic should work, as *...* pairs remained valid"
    assert str(res) == "*not-bold but italic inside**"


def test_escape_inner_not_outer():
    r"""**bold \*escaped* text** — escaped inner, outer works"""
    res = markdown("**bold \\*escaped\\* text**")
    assert isinstance(res, Format)
    assert str(res) == "bold *escaped* text"
    data = res.as_data()
    # Should be bold, but not italic
    types = [item.get("type") for item in data.get("items", [])]
    assert "bold" in types
    assert "italic" not in types


def test_escape_mixed_nested():
    r"""**bold *italic \*escaped\* text*** — escaping inside nested structure"""
    res = markdown("**bold *italic \\*escaped\\* text***")

    assert isinstance(res, Format)
    # Stars around escaped remain in the string as they were escaped.
    # Outer markers ** and * successfully closed via triple.
    assert str(res) == "bold italic *escaped* text"

    data = res.as_data()
    types = {item.get("type") for item in data.get("items", [])}
    assert "bold" in types, "Outer bold should work"
    assert "italic" in types, "Inner italic should work"


def test_escape_in_url_text():
    r"""[text \*with star\*](url) — escaping inside link text"""
    res = markdown("[text \\*star\\*](https://example.com)")

    # 1. Parser should recognize the link and return Format
    assert isinstance(res, Format)

    # 2. Visible text should contain stars (they were escaped)
    # and should not contain markdown markers
    assert str(res) == "text *star*"

    # 3. Escaped stars should NOT create formatting
    data = res.as_data()
    types = {item.get("type") for item in data.get("items", [])}
    assert "italic" not in types

    # 4. URL should be correctly passed in data (this is already an integration check)
    url_items = [i for i in data.get("items", []) if i.get("type") == "url"]
    assert len(url_items) == 1
    assert url_items[0].get("url") == "https://example.com"


# === NEW TESTS: Underline and URL with nesting ===


def test_underline_with_nested_italic():
    """<u>underline *italic*</u> — italic inside underline"""
    res = markdown("<u>underline *italic*</u>")
    assert isinstance(res, Format)
    assert str(res) == "underline italic"
    data = res.as_data()
    types = [item.get("type") for item in data.get("items", [])]
    assert "underline" in types
    assert "italic" in types


def test_url_with_bold_text():
    """[**bold link**](https://example.com) — bold inside link text"""
    res = markdown("[**bold link**](https://example.com)")
    assert isinstance(res, Format)

    data = res.as_data()
    items = data.get("items", [])

    # 1. Check presence of both formats in flat list
    types = {item["type"] for item in items}
    assert "url" in types
    assert "bold" in types

    # 2. Check nesting via offset/length overlap (standard VK API)
    url_item = next(i for i in items if i.get("type") == "url")
    bold_item = next(i for i in items if i.get("type") == "bold")

    url_start = url_item["offset"]
    url_end = url_start + url_item["length"]
    bold_start = bold_item["offset"]
    bold_end = bold_start + bold_item["length"]

    # bold should be fully inside url range
    assert bold_start >= url_start, "Bold should start inside link"
    assert bold_end <= url_end, "Bold should end inside link"

    # 3. Visible text should be correct (no markers)
    assert str(res) == "bold link"


# === NEW TESTS: Boundary Cases ===


def test_unclosed_bold_fallback():
    """**unclosed — unclosed tag returns as text"""
    res = markdown("text **unclosed")
    assert isinstance(res, str)
    assert res == "text **unclosed"


def test_empty_formatting():
    """Raw markers without content do not create formatting."""
    # Naked markers return as plain string
    assert markdown("****") == "****"
    assert isinstance(markdown("****"), str)

    # Space is considered content → formatting applies
    assert isinstance(markdown("** **"), Format)
    assert str(markdown("** **")) == " "


def test_triple_markers_with_content():
    """***text*** — triple markers correctly close nesting."""
    res = markdown("***text***")
    assert isinstance(res, Format)
    assert str(res) == "text"

    # Optionally: check that nested structure was created
    data = res.as_data()
    types = {item["type"] for item in data.get("items", [])}
    assert "bold" in types
    assert "italic" in types


def test_unclosed_trailing_markers():
    """a**** — unclosed markers near text become literals."""
    res = markdown("a****")
    assert isinstance(res, str)
    assert res == "a****"

    # Make sure markers didn't "eat" adjacent text
    assert markdown("text***") == "text***"


def test_alternative_markers():
    """__bold__ and ~~strikethrough~~ (if supported)"""
    # Testing only __bold__, as ~~ is not in spec yet
    res = markdown("__alternative bold__")
    assert isinstance(res, Format)
    assert str(res) == "alternative bold"
    data = res.as_data()
    assert any(item.get("type") == "bold" for item in data.get("items", []))


def test_mixed_underscore_asterisk():
    """**bold** and __also bold__ — mixed markers"""
    res = markdown("**first** and __second__")
    assert isinstance(res, Format)
    assert str(res) == "first and second"
    data = res.as_data()
    bold_count = sum(1 for i in data.get("items", []) if i.get("type") == "bold")
    assert bold_count == 2


def test_emojis_inside_formatting():
    """Emojis inside formatting do not break parsing and offset."""
    res = markdown("**🔥fire🔥**")
    assert isinstance(res, Format)
    assert str(res) == "🔥fire🔥"
    data = res.as_data()
    bold_item = next(i for i in data["items"] if i["type"] == "bold")
    # offset=0, length=7 (🔥 + fire + 🔥) → Python counts emoji as 1 char, VK API too
    assert bold_item["length"] == len("🔥fire🔥")


def test_cyrillic_and_mixed_unicode():
    """Cyrillic, Latin and symbols work the same."""
    res = markdown("**привет world!** *test\\_1*")
    assert str(res) == "привет world! test_1"
    assert isinstance(res, Format)


def test_newlines_preserved():
    """Newlines inside formatting are preserved."""
    res = markdown("**line1\nline2**")
    assert isinstance(res, Format)
    assert str(res) == "line1\nline2"


def test_spaces_as_content():
    """Spaces around text are considered content, formatting applies."""
    res = markdown("** bold text **")
    assert isinstance(res, Format)
    assert str(res) == " bold text "


def test_trailing_backslash():
    """Single backslash at end of string is correctly escaped."""
    assert markdown("text\\") == "text\\"


def test_multiple_backslashes():
    """Escaping backslashes works according to spec."""
    # 1. Pair of backslashes escapes itself: \\ -> \
    assert markdown(r"\\") == "\\"

    # 2. Four backslashes -> two backslashes in output
    assert markdown(r"\\\\") == "\\\\"

    # 3. \* -> literal star (plain text, no formatting)
    assert markdown(r"\*star\*") == "*star*"

    # 4. \\* -> backslash + opening tag (italic applies to text)
    res = markdown(r"\\\\\\*italic\\*")
    assert str(res) == "\\\\\\italic\\"
    assert res.type == "italic"


def test_escaped_at_boundaries():
    """Escaping at start/end of tag."""
    res = markdown("**\\*escaped\\***")
    assert str(res) == "*escaped*"
    assert isinstance(res, Format)
    data = res.as_data()
    assert "italic" not in {i["type"] for i in data["items"]}


def test_url_with_encoded_chars():
    """URL with parameters and special chars."""
    res = markdown("[search](https://example.com?q=hello+world&a=1)")
    assert isinstance(res, Format)
    assert "https://example.com?q=hello+world&a=1" in res.as_raw_data()


def test_url_with_formatting_inside():
    """Formatting inside link text."""
    res = markdown("[*italic* and **bold**](https://vk.com)")
    assert isinstance(res, Format)
    assert str(res) == "italic and bold"

    data = res.as_data()
    types = {i["type"] for i in data["items"]}

    assert "url" in types
    assert "italic" in types
    assert "bold" in types


def test_empty_and_whitespace_only():
    """Empty strings and whitespace-only strings return unchanged."""
    assert markdown("") == ""
    assert markdown("   ") == "   "
    assert isinstance(markdown("   "), str)


def test_interleaved_markers_fallback():
    """**a*b**c* — valid Markdown does not allow intersection, parser should return predictable text."""
    markdown("**a*b**c*")
