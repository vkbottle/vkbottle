from vkbottle.tools import Formatter, bold, italic, underline, url


def test_docs_formatter():
    f1 = Formatter("{:bold}, nice formatting!").format("Wow")
    assert f1.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "bold", "offset": 0, "length": 3}],
    }

    f2 = Formatter("{framework:italic} has been around for over 5 years!").format(
        framework="vkbottle"
    )
    assert f2.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 0, "length": 8}],
    }

    f3 = Formatter("Very cool {:bold+italic} ^_^").format("bold-italic message")
    assert f3.format_data == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 10, "length": 19},
            {"type": "italic", "offset": 10, "length": 19},
        ],
    }

    f4 = Formatter("My bestie is {bestie:underline}").format_map({"bestie": "telegrinder"})
    assert f4.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "underline", "offset": 13, "length": 11}],
    }


def test_docs_funcs():
    s1 = bold("Hello, ") + italic("World!")
    assert s1.as_data() == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 0, "length": 7},
            {"type": "italic", "offset": 7, "length": 6},
        ],
    }

    s2 = "Hello, " + italic("World!")
    assert s2.as_data() == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 7, "length": 6}],
    }

    s3 = bold("Hello") + ", " + italic("World!")
    assert s3.as_data() == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 0, "length": 5},
            {"type": "italic", "offset": 7, "length": 6},
        ],
    }

    s4 = (
        bold("vkbottle documentation:")
        + " "
        + url(italic("click me"), href="vkbottle.readthedocs.io/ru/latest")
    )
    assert s4.as_data() == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 0, "length": 23},
            {
                "type": "url",
                "offset": 24,
                "length": 8,
                "url": "vkbottle.readthedocs.io/ru/latest",
            },
            {"type": "italic", "offset": 24, "length": 8},
        ],
    }


def test_utf16_formatter():
    s1 = Formatter("{:bold}, 🌍").format("Hello")
    assert s1.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "bold", "offset": 0, "length": 5}],
    }

    s2 = Formatter("👋, {:bold}!").format("world")
    assert s2.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "bold", "offset": 4, "length": 5}],
    }

    s3 = Formatter("😊{:italic}").format("face")
    assert s3.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 2, "length": 4}],
    }

    s4 = Formatter("{:bold}x😊x{:italic}").format("Smily", "face")
    assert s4.format_data == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 0, "length": 5},
            {"type": "italic", "offset": 9, "length": 4},
        ],
    }

    s5 = Formatter("🌟Reach the {:bold}\nFly me to the 🚀 {:italic+bold}!").format(
        "stars!", "moon"
    )
    assert s5.format_data == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 12, "length": 6},
            {"type": "italic", "offset": 36, "length": 4},
            {"type": "bold", "offset": 36, "length": 4},
        ],
    }

    s6 = Formatter("Café ☕️ - xx{from_french:underline}xx").format_map(
        {"from_french": "is a Cafe!"}
    )
    assert s6.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "underline", "offset": 12, "length": 10}],
    }

    s7 = Formatter("😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😙😚 - a x{:italic}x of emojies").format("bunch")
    assert s7.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 40, "length": 5}],
    }

    s8 = Formatter("こんにちは ({japanize:italic}) 🌸").format_map({"japanize": "Konnichiwa"})
    assert s8.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 7, "length": 10}],
    }

    s9 = Formatter("{:underline}").format("underlined 🌸")
    assert s9.format_data == {
        "version": Formatter.VERSION,
        "items": [{"type": "underline", "offset": 0, "length": 12}],
    }


def test_utf16_format_func():
    s1 = bold("Hello") + ", 🌍"
    assert s1.as_data() == {
        "version": Formatter.VERSION,
        "items": [{"type": "bold", "offset": 0, "length": 5}],
    }

    s2 = "👋, " + bold("world")
    assert s2.as_data() == {
        "version": Formatter.VERSION,
        "items": [{"type": "bold", "offset": 4, "length": 5}],
    }

    s3 = "😊" + italic("face")
    assert s3.as_data() == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 2, "length": 4}],
    }

    s4 = bold("smily") + "x😊x" + italic("face")
    assert s4.as_data() == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 0, "length": 5},
            {"type": "italic", "offset": 9, "length": 4},
        ],
    }

    s5 = "🌟Reach the " + bold("stars!") + "\nFly me to the 🚀 " + italic(bold("moon")) + "!"
    assert s5.as_data() == {
        "version": Formatter.VERSION,
        "items": [
            {"type": "bold", "offset": 12, "length": 6},
            {"type": "italic", "offset": 36, "length": 4},
            {"type": "bold", "offset": 36, "length": 4},
        ],
    }

    from_french = "is a Cafe!"
    s6 = "Café ☕️ - xx" + underline(from_french) + "xx"
    assert s6.as_data() == {
        "version": Formatter.VERSION,
        "items": [{"type": "underline", "offset": 12, "length": 10}],
    }

    s7 = "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😙😚 - a x" + italic("bunch") + "x of emojies"
    assert s7.as_data() == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 40, "length": 5}],
    }

    japanize = "Konnichiwa"
    s8 = "こんにちは (" + italic(japanize) + ") 🌸"
    assert s8.as_data() == {
        "version": Formatter.VERSION,
        "items": [{"type": "italic", "offset": 7, "length": 10}],
    }


def test_functional_equivalence():
    funcs_1 = bold("Hello") + ", 🌍"
    formatter_1 = Formatter("{:bold}, 🌍").format("Hello")
    assert funcs_1.as_data() == formatter_1.format_data

    funcs_2 = "👋, " + bold("world")
    formatter_2 = Formatter("👋, {:bold}!").format("world")
    assert funcs_2.as_data() == formatter_2.format_data

    funcs_3 = "😊" + italic("face")
    formatter_3 = Formatter("😊{:italic}").format("face")
    assert funcs_3.as_data() == formatter_3.format_data

    funcs_4 = bold("smily") + "x😊x" + italic("face")
    formatter_4 = Formatter("{:bold}x😊x{:italic}").format("smily", "face")
    assert funcs_4.as_data() == formatter_4.format_data

    funcs_5 = "🌟Reach the " + bold("stars!") + "\nFly me to the 🚀 " + italic(bold("moon")) + "!"
    formatter_5 = Formatter("🌟Reach the {:bold}\nFly me to the 🚀 {:italic+bold}!").format(
        "stars!", "moon"
    )
    assert funcs_5.as_data() == formatter_5.format_data

    from_french = "is a Cafe!"
    funcs_6 = "Café ☕️ - xx" + underline(from_french) + "xx"
    formatter_6 = Formatter("Café ☕️ - xx{from_french:underline}xx").format_map(
        {"from_french": from_french}
    )
    assert funcs_6.as_data() == formatter_6.format_data

    funcs_7 = "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😙😚 - a x" + italic("bunch") + "x of emojies"
    formatter_7 = Formatter(
        "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘😗😙😚 - a x{:italic}x of emojies"
    ).format("bunch")
    assert funcs_7.as_data() == formatter_7.format_data

    japanize = "Konnichiwa"
    funcs_8 = "こんにちは (" + italic(japanize) + ") 🌸"
    formatter_8 = Formatter("こんにちは ({japanize:italic}) 🌸").format_map({"japanize": japanize})
    assert funcs_8.as_data() == formatter_8.format_data
