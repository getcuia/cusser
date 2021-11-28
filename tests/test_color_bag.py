"""Tests for the color bag class."""

import curses

import ochre
import pytest

from cusser._color_bag import ColorBag


@pytest.fixture
def stdscr():
    """Return a curses screen."""
    stdscr = curses.initscr()
    curses.start_color()
    yield stdscr


def test_color_bag_add_color(stdscr):
    """Test adding a color to the color bag."""
    color_bag = ColorBag()
    color_bag.add(ochre.Hex("#ff0000"))
    assert list(color_bag.colors) == [ochre.RGB(1, 0, 0)]
    assert len(color_bag) == 1
    assert ochre.RGB(1, 0, 0) in color_bag


def test_color_bag_discard_color(stdscr):
    """Test discarding a color from the color bag."""
    color_bag = ColorBag()
    color_bag.add(ochre.Hex("#ff0000"))
    color_bag.discard(ochre.Hex("#ff0000"))
    assert list(color_bag.colors) == []
    assert len(color_bag) == 0
    assert ochre.RGB(1, 0, 0) not in color_bag
