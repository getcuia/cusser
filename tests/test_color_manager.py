"""Tests for the color manager class."""


import ochre

from cusser.color_manager import ColorManager


def test_color_manager_add_color():
    """Test adding a color to the color manager."""
    color_manager = ColorManager()
    color_manager.add(ochre.Hex("#ff0000"))
    assert list(color_manager.colors) == [ochre.RGB(1, 0, 0)]
    assert len(color_manager) == 1
    assert ochre.RGB(1, 0, 0) in color_manager


def test_color_manager_discard_color():
    """Test discarding a color from the color manager."""
    color_manager = ColorManager()
    color_manager.add(ochre.Hex("#ff0000"))
    color_manager.discard(ochre.Hex("#ff0000"))
    assert list(color_manager.colors) == []
    assert len(color_manager) == 0
    assert ochre.RGB(1, 0, 0) not in color_manager
