"""General tests."""

import curses

from cusser import Cusser, __version__


def test_version():
    """Ensure the version is correct."""
    assert __version__ == "0.1.0"


def test_cusser():
    """Ensure the wrapper works."""

    def _app(stdscr):
        stdscr = Cusser(stdscr)
        text = "\033[1;5;33mHello \033[2mWorld\033[0m!"
        stdscr.addstr(text)
        stdscr.refresh()
        stdscr.getch()

    _app(curses.initscr())
