from vkbottle.tools.formatting import Format, markdown


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
