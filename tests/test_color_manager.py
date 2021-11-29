"""Tests for the color bag class."""

import curses

import ochre
import pytest

from cusser._color_manager import ColorManager


@pytest.fixture
def stdscr():
    """Return a curses screen."""
    stdscr = curses.initscr()
    curses.start_color()
    yield stdscr


def test_color_manager_add_color(stdscr):
    """Test adding a color to the color bag."""
    color_manager = ColorManager()
    color_manager.add(ochre.Hex("#ff0000"))
    assert list(color_manager.colors) == [ochre.RGB(1, 0, 0)]
    assert len(color_manager) == 1
    assert ochre.RGB(1, 0, 0) in color_manager


def test_color_manager_discard_color(stdscr):
    """Test discarding a color from the color bag."""
    color_manager = ColorManager()
    color_manager.add(ochre.Hex("#ff0000"))
    color_manager.discard(ochre.Hex("#ff0000"))
    assert list(color_manager.colors) == []
    assert len(color_manager) == 0
    assert ochre.RGB(1, 0, 0) not in color_manager
