"""Run a simple test of the Cusser class."""


import curses
from functools import reduce

from ._misc import _SUPPORTED_STYLE_TAGS, _app

if __name__ == "__main__":
    message = "The quick brown fox jumps over the lazy dog"
    text = reduce(
        lambda acc, style: acc + style(message) + "\n", _SUPPORTED_STYLE_TAGS, ""
    )
    curses.wrapper(lambda stdscr: _app(stdscr, text))
