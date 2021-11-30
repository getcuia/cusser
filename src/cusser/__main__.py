"""Run a simple test of the Cusser class."""


import curses
import sys
from functools import reduce

from ._misc import _SUPPORTED_ATTRIBUTE_TAGS, _SUPPORTED_COLOR_TAGS, _app

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            f"usage: {sys.argv[0]} <example>, where <example> is one of: "
            "'attributes', 'colors', 'clear', 'cursor'"
        )
        sys.exit(1)

    message = "The quick brown fox jumps over the lazy dog"

    if sys.argv[1] == "attributes":
        text = reduce(
            lambda acc, attribute: acc + attribute(message) + "\n",
            _SUPPORTED_ATTRIBUTE_TAGS,
            "",
        )
    elif sys.argv[1] == "colors":
        text = reduce(
            lambda acc, color: acc + color(message) + "\n", _SUPPORTED_COLOR_TAGS, ""
        )
    elif sys.argv[1] == "clear":
        text = f"{message}\033[2JScreen cleared!\n{message}\033[2K"
    elif sys.argv[1] == "cursor":
        text = f"{message}\033[H\033[B\033[C{message}\033[3;3H{message}"
    else:
        raise ValueError(
            f"unknown example: {sys.argv[1]}, must be one of: "
            "'attributes', 'colors', 'clear', 'cursor'"
        )

    curses.wrapper(lambda stdscr: _app(stdscr, text))
