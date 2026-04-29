from __future__ import annotations

import dataclasses
import re

import typing_extensions as typing

from vkbottle.modules import json

FormatType: typing.TypeAlias = typing.Literal[
    "bold",
    "italic",
    "underline",
    "url",
]

FORMAT_PATTERN = re.compile(
    r"\{\}|\{(?:(?P<name>\w+)(?::(?P<formats1>\w+(?:\+\w+)*))?|:(?P<formats2>\w+(?:\+\w+)*))\}"
)

# Precompiled pattern for Markdown parsing (module-level, MVP).
_MARKDOWN_PATTERN = re.compile(
    # Priority: URL inline first, so [text](url) matches reliably inside markdown
    r"(?<!\\)\[(?P<text>[^]]+)\]\((?P<href>[^)]+)\)|"
    r"(?<!\\)<u>(?P<underline_tag>.+?)</u>|"
    r"(?<!\\)\*\*(?P<bold>.+?)\*\*|(?<!\\)__(?P<bold2>.+?)__|"
    r"(?<!\\)\*(?P<italic>.+?)\*(?!\*)|(?<!\\)_(?P<italic2>.+?)_(?!_)"
)


def _unescape_text(text: str) -> str:
    """Unescape common Markdown escapes in plain text parts.

    We remove the escaping backslashes that were used to escape Markdown
    characters so that the final output shows the literal characters.
    This affects only plain text segments, not Format objects.
    """
    t = text
    # Normalize backslashes first, then unescape common Markdown chars
    t = t.replace("\\\\", "\\")
    t = t.replace("\\*", "*")
    t = t.replace("\\[", "[")
    t = t.replace("\\]", "]")
    t = t.replace("\\`", "`")
    t = t.replace("\\_", "_")
    return t


def _calculate_offset(string: str) -> int:
    # https://dev.vk.ru/en/reference/objects/message#format_data
    return len(string.encode("utf-16-le")) // 2


def _format(
    string: str | Format,
    fmt_type: FormatType,
    data: dict[str, typing.Any] | None = None,
    /,
) -> Format:
    data = data or {}

    if isinstance(string, Format):
        return Format(string.string, type=fmt_type, data=data, other_formats=[string])
    return Format(string, type=fmt_type, data=data)


def bold(string: str | Format, /) -> Format:
    return _format(string, "bold")


def italic(string: str | Format, /) -> Format:
    return _format(string, "italic")


def underline(string: str | Format, /) -> Format:
    return _format(string, "underline")


def markdown(string: str) -> str | Format:
    """Regex-based Markdown parsing (MVP, one level, no nesting).

    Supported: bold (**text** / __text__), italic (*text* / _text_),
    underline via <u>text</u> (HTML tag), and links [text](url).

    Escaping:
    - Backslashes before formatting markers are respected by the parser.
    - After final assembly, we unescape certain plain text portions so the
        final output looks correct to users.

        VK specifics:
        - Leading asterisk tokens like *vkbottle at word start may be
            interpreted by VK as a link to
            https://vk.com/vkbottle. This is VK's behavior, not our parser.
        - If the text after the star is not a nickname, VK may still interpret
            differently (for example, leading to user or community pages).

    Returns: either a string or a Format object.
    """
    s = string

    # Build token stream using module-level precompiled pattern
    pattern = _MARKDOWN_PATTERN

    parts: list[str | Format] = []
    last = 0

    for m in pattern.finditer(s):
        start, end = m.span()
        if start > last:
            parts.append(_unescape_text(s[last:start]))

        if m.group("underline_tag") is not None:
            inner = m.group("underline_tag")
            parts.append(underline(inner))
        elif m.group("bold") is not None or m.group("bold2") is not None:
            inner = m.group("bold") if m.group("bold") is not None else m.group("bold2")
            parts.append(bold(inner))
        elif m.group("italic") is not None or m.group("italic2") is not None:
            inner = m.group("italic") if m.group("italic") is not None else m.group("italic2")
            parts.append(italic(inner))
        elif m.group("text") is not None:
            inner = m.group("text")
            href = m.group("href")
            parts.append(url(inner, href=href))
        else:
            parts.append(s[start:end])

        last = end

    if last < len(s):
        parts.append(_unescape_text(s[last:]))

    if not parts:
        return s

    result = parts[0]
    for part in parts[1:]:
        result = result + part  # type: ignore[assignment]

    return result


def url(string: str | Format, /, *, href: str) -> Format:
    return _format(string, "url", {"url": href})


@dataclasses.dataclass
class Format:
    string: str
    type: FormatType
    offset: int = dataclasses.field(init=False)
    length: int = dataclasses.field(init=False)
    data: dict[str, typing.Any] = dataclasses.field(default_factory=dict[str, typing.Any])
    other_formats: list[typing.Self] = dataclasses.field(default_factory=list[typing.Self])

    def __post_init__(self) -> None:
        self.offset = 0
        self.length = len(self.string)

    def __str__(self) -> str:
        return self.string

    def __add__(self, other: object, /) -> typing.Self:
        if not isinstance(other, (str, self.__class__)):
            return NotImplemented
        if isinstance(other, str):
            self.string += other
            return self
        return self.add_other(other)

    def __iadd__(self, other: object, /) -> typing.Self:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.add_other(other)

    def __radd__(self, other: object, /) -> typing.Self:
        if not isinstance(other, str):
            return NotImplemented
        if isinstance(other, str):
            rhs_offset = _calculate_offset(other)
            self.offset += rhs_offset
            for other_format in self.other_formats:
                other_format.offset += rhs_offset
            self.string = other + self.string
            return self

        self.string += other
        return self

    def add_other(self, other: typing.Self, /) -> typing.Self:
        rhs_offset = _calculate_offset(self.string)
        other.offset += rhs_offset
        for other_format in other.other_formats:
            other_format.offset += rhs_offset

        self.string += other.string
        self.other_formats.append(other)
        return self

    def as_data(
        self,
        *,
        offset: int = 0,
        version: int | None = None,
    ) -> dict[str, typing.Any]:
        result = {
            "version": Formatter.VERSION if version is None else version,
            "items": [
                {
                    "type": self.type,
                    "offset": self.offset + offset,
                    "length": self.length,
                    **self.data,
                }
            ],
        }

        if not self.other_formats:
            return result

        for fmt in self.other_formats:
            result["items"].extend(fmt.as_data(offset=offset)["items"])  # type: ignore

        return result

    def as_raw_data(self, *, offset: int = 0) -> str:
        return json.dumps(self.as_data(offset=offset))


class Formatter(str):
    format_data: dict[str, typing.Any]

    __slots__ = ("format_data",)

    VERSION: typing.ClassVar[int] = 1
    FORMATS: typing.ClassVar[dict[str, typing.Callable[[str], Format]]] = {
        "bold": bold,
        "italic": italic,
        "underline": underline,
    }

    def __new__(cls, string: str = "", /) -> typing.Self:
        formatter = super().__new__(cls, string)
        formatter.format_data = {"version": cls.VERSION, "items": []}
        return formatter

    def format(self, *args: typing.Any, **kwargs: typing.Any) -> Formatter:
        output = ""
        items = []
        arg_index = last_end = 0

        for match in FORMAT_PATTERN.finditer(self):
            name = match.group("name")
            formats = match.group("formats1") or match.group("formats2")
            start, end = match.span()

            output += self[last_end:start]
            offset = _calculate_offset(output)

            if name is None:
                value = args[arg_index]
                arg_index += 1
            else:
                value = kwargs[name]

            if isinstance(value, Format):
                items.extend(value.as_data(offset=offset)["items"])
                value = value.string
            else:
                value = str(value)

            if formats:
                for fmt in formats.split("+"):
                    if fmt not in self.__class__.FORMATS:
                        raise ValueError(
                            "Unknown format `{}`, available formats: {}.".format(  # noqa: EM103
                                fmt,
                                ", ".join(f"`{x}`" for x in self.__class__.FORMATS),
                            ),
                        )

                    formatter = self.__class__.FORMATS[fmt]
                    items.extend(formatter(value).as_data(offset=offset)["items"])

            output += value
            last_end = end

        output += self[last_end:]
        formatted = self.__class__(output)
        formatted.format_data["items"].extend(items)
        return formatted

    def format_map(self, mapping: typing.Mapping[str, typing.Any], /) -> Formatter:  # type: ignore
        return self.format(**mapping)

    @property
    def raw_format_data(self) -> str:
        return json.dumps(self.format_data)


__all__ = ("Format", "Formatter", "bold", "italic", "underline", "url")
