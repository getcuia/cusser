"""Run a simple test of the Cusser class."""


import curses
from functools import reduce
from typing import Callable, Text

from stransi import Ansi

from . import Cusser

if __name__ == "__main__":

    def _tag(start: Text, end: Text = "\033[0m") -> Callable[[Text], Ansi]:
        def decorator(text: Text) -> Ansi:
            return Ansi(f"{start}{text}{end}")

        return decorator

    normal = _tag("\033[0m", "")
    bold = _tag("\033[1m", "\033[22m")
    dim = _tag("\033[2m", "\033[22m")
    italic = _tag("\033[3m", "\033[23m")
    underline = _tag("\033[4m", "\033[24m")
    blink = _tag("\033[5m", "\033[25m")
    reverse = _tag("\033[7m", "\033[27m")
    hidden = _tag("\033[8m", "\033[28m")

    ALL_STYLES = (normal, bold, dim, italic, underline, blink, reverse, hidden)

    def _app(stdscr):
        stdscr = Cusser(stdscr)
        message = "The quick brown fox jumps over the lazy dog"
        text = reduce(lambda acc, style: acc + style(message) + "\n", ALL_STYLES, "")
        stdscr.addstr(text)
        stdscr.refresh()
        stdscr.getch()

    curses.wrapper(_app)
