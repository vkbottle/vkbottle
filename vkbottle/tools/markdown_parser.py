"""Markdown parser for VK formatting.

Converts Markdown text to VK Format objects via a stack-based parser.
Supports **bold**, *italic*, <u>underline</u>, and [url](link) as limited by VK API.
Escapes are honored; nested formatting is supported.
"""

from __future__ import annotations

import dataclasses
import re
from typing import NamedTuple, cast

from .formatting import Format, bold, italic, underline, url

_FMT_MAP = {"bold": bold, "italic": italic, "u": underline}

_TOKEN_RE = re.compile(
    r"(?P<esc>\\.)|"
    r"(?P<bs>\\)|"
    r"(?P<triple>\*\*\*|___)|"
    r"(?P<bold>\*\*|__)|"
    r"(?P<italic>[*_])|"
    r"(?P<u_open><u>)|"
    r"(?P<u_close></u>)|"
    r"(?P<url_open>\[)|"
    r"(?P<url_mid>\]\()|"
    r"(?P<url_close>\))|"
    r"(?P<text>[^\*__\[\]()<>\\]+)"
)


class Token(NamedTuple):
    type: str
    value: str


@dataclasses.dataclass
class StackFrame:
    ctx_type: str | None
    parts: list[str | Format] = dataclasses.field(default_factory=list)
    url_data: str | Format | None = None
    open_marker: str = ""


def _tokenize(text: str) -> list[Token]:
    return [Token(cast("str", m.lastgroup), m.group()) for m in _TOKEN_RE.finditer(text)]


def _unescape(text: str) -> str:
    return (
        text.replace("\\*", "*")
        .replace("\\_", "_")
        .replace("\\[", "[")
        .replace("\\]", "]")
        .replace("\\`", "`")
    )


def _join(parts: list[str | Format]) -> str | Format:
    if not parts:
        return ""
    res = parts[0]
    for p in parts[1:]:
        res = p.__radd__(res) if isinstance(res, str) and isinstance(p, Format) else res + p
    return res


def _close_frame(stack: list[StackFrame], closing_marker: str) -> None:
    """Close the current formatting frame.

    If the frame has no content, emit the literal markers as text.
    """
    frame = stack.pop()
    inner = _join(frame.parts)
    if inner:
        stack[-1].parts.append(_FMT_MAP[cast("str", frame.ctx_type)](inner))
    else:
        stack[-1].parts.append(frame.open_marker + closing_marker)


def _handle_triple(stack: list[StackFrame]) -> None:
    """Handle triple markers (*** or ___): manage bold and italic contexts."""
    ctx = stack[-1]

    if ctx.ctx_type in ("bold", "italic"):
        inner = _join(ctx.parts)
        popped = stack.pop()  # Save the closed frame
        if inner:
            # Add format to the parent frame
            stack[-1].parts.append(_FMT_MAP[cast("str", popped.ctx_type)](inner))
        else:
            closer = "**" if popped.ctx_type == "bold" else "*"
            stack[-1].parts.append(popped.open_marker + closer)
        rem_type = "italic" if popped.ctx_type == "bold" else "bold"
    else:
        # No open context -> open bold first
        stack.append(StackFrame("bold", open_marker="**"))
        rem_type = "italic"

    # Process the remaining part of the triple marker
    top = stack[-1]
    if top.ctx_type == rem_type:
        inner2 = _join(top.parts)
        popped2 = stack.pop()
        if inner2:
            stack[-1].parts.append(_FMT_MAP[rem_type](inner2))
        else:
            closer2 = "*" if rem_type == "italic" else "**"
            stack[-1].parts.append(popped2.open_marker + closer2)
    else:
        # Open new context for the remaining part
        marker = "*" if rem_type == "italic" else "**"
        stack.append(StackFrame(rem_type, open_marker=marker))


def _handle_literal(token: Token, stack: list[StackFrame]) -> None:
    """Process escapes, backslashes, and literal text."""
    ctx = stack[-1]
    if token.type == "esc":
        ctx.parts.append(token.value[1])
    elif token.type == "bs":
        ctx.parts.append("\\")
    else:
        ctx.parts.append(token.value)


def _handle_format(token: Token, stack: list[StackFrame]) -> None:
    """Handle bold/italic with strict marker matching."""
    ctx = stack[-1]
    fmt_type = token.type  # "bold" or "italic"

    if ctx.ctx_type == fmt_type and ctx.open_marker == token.value:
        _close_frame(stack, token.value)
    else:
        stack.append(StackFrame(fmt_type, open_marker=token.value))


def _handle_underline(token: Token, stack: list[StackFrame]) -> None:
    """Handle opening/closing <u> and </u>."""
    ctx = stack[-1]
    if token.type == "u_open":
        stack.append(StackFrame("u", open_marker="<u>"))
    elif ctx.ctx_type == "u":
        _close_frame(stack, token.value)
    else:
        ctx.parts.append("<u>")


def _handle_url(token: Token, stack: list[StackFrame]) -> None:
    """Process URL states: open, text, href, close."""
    ctx = stack[-1]
    if token.type == "url_open":
        stack.append(StackFrame("url_text", open_marker="["))
    elif token.type == "url_mid" and ctx.ctx_type == "url_text":
        link_text = _join(ctx.parts)
        stack.pop()
        stack.append(StackFrame("url_href", url_data=link_text))
    elif token.type == "url_close" and ctx.ctx_type == "url_href":
        href_raw = _join(ctx.parts)
        lt_raw = ctx.url_data

        close_link_text: str | Format = lt_raw if lt_raw is not None else ""
        if isinstance(close_link_text, str):
            close_link_text = _unescape(close_link_text)

        href_str = str(href_raw)
        href_str = _unescape(href_str)

        stack.pop()
        stack[-1].parts.append(url(close_link_text, href=href_str))


def _process_token(token: Token, stack: list[StackFrame]) -> None:
    """Dispatch token to the appropriate handler."""
    match token.type:
        case "esc" | "bs" | "text":
            _handle_literal(token, stack)
        case "bold" | "italic":
            _handle_format(token, stack)
        case "triple":
            _handle_triple(stack)
        case "u_open" | "u_close":
            _handle_underline(token, stack)
        case "url_open" | "url_mid" | "url_close":
            _handle_url(token, stack)


def _apply_fallback(stack: list[StackFrame]) -> None:
    """Convert unclosed frames into literal text."""
    while len(stack) > 1:
        frame = stack.pop()
        if frame.ctx_type in ("url_text", "url_href"):
            marker = "[" if frame.ctx_type == "url_text" else f"[{frame.url_data or ''}]("
            stack[-1].parts.append(marker)
            stack[-1].parts.extend(frame.parts)
            if frame.ctx_type == "url_text":
                stack[-1].parts.append("](")
            else:
                stack[-1].parts.append(")")
            continue
        if frame.ctx_type not in _FMT_MAP:
            continue

        stack[-1].parts.append(frame.open_marker)
        stack[-1].parts.extend(frame.parts)


def markdown(string: str) -> str | Format:
    """Parse a Markdown string into VK Format objects.

    Supports **bold**, *italic*, <u>underline</u>, and [url](link) markup,
    which are the formatting options available in VK API.

    Examples:
        Single-level formatting:
        >>> markdown("**Hello** world")

        Nested formatting:
        >>> markdown("**bold *italic*** text")
    """
    tokens = _tokenize(string)
    stack: list[StackFrame] = [StackFrame(ctx_type=None)]

    for token in tokens:
        _process_token(token, stack)

    _apply_fallback(stack)

    root_parts = stack[0].parts
    if not root_parts:
        return ""

    result = _join(root_parts)

    if isinstance(result, Format):
        return result if result.string else ""

    return _unescape(result)
