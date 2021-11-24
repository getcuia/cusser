"""General tests."""

import curses
from functools import reduce

from cusser import __version__
from cusser._misc import _SUPPORTED_COLOR_TAGS, _SUPPORTED_STYLE_TAGS, _app


def test_version():
    """Ensure the version is correct."""
    assert __version__ == "0.1.0"


def test_styles():
    """Ensure styles don't break."""
    message = "The quick brown fox jumps over the lazy dog"
    text = reduce(
        lambda acc, style: acc + style(message) + "\n", _SUPPORTED_STYLE_TAGS, ""
    )
    _app(curses.initscr(), text)


def test_colors():
    """Ensure colors don't break."""
    message = "The quick brown fox jumps over the lazy dog"
    text = reduce(
        lambda acc, color: acc + color(message) + "\n", _SUPPORTED_COLOR_TAGS, ""
    )
    _app(curses.initscr(), text)
