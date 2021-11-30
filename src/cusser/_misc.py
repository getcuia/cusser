"""Private miscellaneous utilities."""


from __future__ import annotations

import curses
from typing import Callable, Text

from stransi import Ansi

from cusser import Cusser


def _tag(start: Text, end: Text = "\033[0m") -> Callable[[Text], Ansi]:
    """Define a tag function for ANSI escape sequences."""

    def decorator(text: Text) -> Ansi:
        return Ansi(f"{start}{text}{end}")

    return decorator


_normal = _tag("\033[0m", "")
_bold = _tag("\033[1m", "\033[22m")
_dim = _tag("\033[2m", "\033[22m")
_italic = _tag("\033[3m", "\033[23m")
_underline = _tag("\033[4m", "\033[24m")
_blink = _tag("\033[5m", "\033[25m")
_reverse = _tag("\033[7m", "\033[27m")
_hidden = _tag("\033[8m", "\033[28m")

_SUPPORTED_ATTRIBUTE_TAGS = (
    _normal,
    _bold,
    _dim,
    _italic,
    _underline,
    _blink,
    _reverse,
    _hidden,
)


def _colortag(start: Text) -> Callable[[Text], Ansi]:
    """Define a tag function for a color ANSI escape sequence."""
    return _tag(start, "\033[39m")


_black = _colortag("\033[90m")
_red = _colortag("\033[91m")
_green = _colortag("\033[92m")
_yellow = _colortag("\033[93m")
_blue = _colortag("\033[94m")
_magenta = _colortag("\033[95m")
_cyan = _colortag("\033[96m")
_white = _colortag("\033[97m")


_SUPPORTED_COLOR_TAGS = (_black, _red, _green, _yellow, _blue, _magenta, _cyan, _white)


def _app(
    stdscr: Cusser | curses._CursesWindow, text: Text | Callable[[], Text]
) -> None:
    """Start a new application for testing."""
    if callable(text):
        text = text()
    if not isinstance(stdscr, Cusser):
        stdscr = Cusser(stdscr)
    stdscr.addstr(text)
    stdscr.refresh()
    stdscr.getch()
