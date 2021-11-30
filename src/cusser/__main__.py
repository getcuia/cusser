"""Run a simple test of the Cusser class."""


import curses
import sys
from functools import reduce

from ._misc import _SUPPORTED_COLOR_TAGS, _SUPPORTED_STYLE_TAGS, _app

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            f"usage: {sys.argv[0]} <example>, where <example> is one of: 'styles', 'colors'"
        )
        sys.exit(1)

    message = "The quick brown fox jumps over the lazy dog"

    if sys.argv[1] == "styles":
        text = reduce(
            lambda acc, style: acc + style(message) + "\n", _SUPPORTED_STYLE_TAGS, ""
        )
    elif sys.argv[1] == "colors":
        text = reduce(
            lambda acc, color: acc + color(message) + "\n", _SUPPORTED_COLOR_TAGS, ""
        )
    else:
        raise ValueError(
            f"unknown example: {sys.argv[1]}, must be one of: 'styles', 'colors'"
        )

    curses.wrapper(lambda stdscr: _app(stdscr, text))
