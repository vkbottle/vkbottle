"""Markdown parser for VK formatting.

Converts Markdown text to VK Format objects via a stack-based parser.
Supports **bold**, *italic*, <u>underline</u>, and [url](link) as limited by VK API.
Escapes are honored; nested formatting is supported.
"""

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


def _resolve_triple(token: Token, stack: list[StackFrame]) -> None:
    """Resolve a pending triple marker on top of the stack.

    Called when the next marker (\\* or \\*\\*) arrives after \\***.
    Handles both full closure (\\*\\*\\* matches \\*\\*\\*) and partial closure.
    """
    ctx = stack[-1]
    parts = ctx.parts
    marker = token.value
    fmt_type = token.type

    # Full closure: *** matches ***
    if marker == ctx.open_marker:
        inner = _join(parts)
        stack.pop()
        # If empty -> literals, otherwise -> nested formatting
        stack[-1].parts.append(bold(italic(inner)) if inner else ctx.open_marker + marker)
        return

    # Partial closure
    rem_type = "italic" if fmt_type == "bold" else "bold"
    remainder = ctx.open_marker[len(marker) :]
    inner = _join(parts)

    if inner:
        # Nest formatted content into remainder (preserve LIFO nesting)
        closed_content = _FMT_MAP[fmt_type](inner)
        stack[-1] = StackFrame(rem_type, parts=[closed_content], open_marker=remainder)
    else:
        # Empty content -> emit literals and remove frame
        stack.pop()
        stack[-1].parts.append(ctx.open_marker + marker)


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
    """Handle bold, italic, and triple markers with lazy resolution.

    1. Resolve pending triple if present on stack top
    2. Handle incoming triple (may close existing context)
    3. Standard open/close for remaining marker (fall-through)
    """

    # Try to resolve pending triple on stack top
    if stack[-1].ctx_type == "triple" and token.value[0] == stack[-1].open_marker[0]:
        _resolve_triple(token, stack)
        return

    # Incoming triple
    if token.type == "triple":
        ctx = stack[-1]

        # Try to close current context if compatible and marker matches
        if ctx.ctx_type in ("bold", "italic") and token.value.startswith(ctx.open_marker):
            _close_frame(stack, ctx.open_marker)
            # Triple remainder always becomes opposite type marker
            marker = token.value[len(ctx.open_marker) :]
            token = Token("italic" if ctx.ctx_type == "bold" else "bold", marker)

    # Standard open/close (handles triple remainder or regular markers)
    ctx = stack[-1]
    if ctx.ctx_type == token.type and ctx.open_marker == token.value:
        _close_frame(stack, token.value)
    else:
        stack.append(StackFrame(token.type, open_marker=token.value))


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
    """Dispatch token to the appropriate handler based on token type."""
    match token.type:
        case "esc" | "bs" | "text":
            _handle_literal(token, stack)
        case "bold" | "italic" | "triple":
            _handle_format(token, stack)
        case "u_open" | "u_close":
            _handle_underline(token, stack)
        case "url_open" | "url_mid" | "url_close":
            _handle_url(token, stack)


def _apply_fallback(stack: list[StackFrame]) -> None:
    """Convert unclosed frames into literal text.

    Handles special cases: url_text/url_href, triple markers, and regular formats.
    """
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

        if frame.ctx_type == "triple":
            stack[-1].parts.append(frame.open_marker)
            stack[-1].parts.extend(frame.parts)
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
            markdown("\\*\\*Hello\\*\\* world")

        Nested formatting:
            markdown("\\*\\*bold \\*italic\\*\\*\\* text")
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
