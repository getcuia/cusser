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

_SUPPORTED_STYLE_TAGS = (
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


_red = _colortag("\033[31m")

_SUPPORTED_COLOR_TAGS = (_red,)


def _app(stdscr: Cusser | curses._CursesWindow, text: Text) -> None:
    """Start a new application for testing."""
    if not isinstance(stdscr, Cusser):
        stdscr = Cusser(stdscr)
    stdscr.addstr(text)
    stdscr.refresh()
    stdscr.getch()
