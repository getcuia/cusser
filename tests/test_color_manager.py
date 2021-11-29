"""Tests for the color manager class."""

import ochre
import pytest

from cusser.color_manager import ColorManager


@pytest.fixture
def color_manager():
    """Return a new ColorManager."""
    return ColorManager()


def test_color_manager(color_manager):
    """Test adding, getting, and removing colors."""
    color_manager.add(ochre.Hex("#ff0000"))

    assert list(color_manager.colors) == [ochre.RGB(1, 0, 0)]

    assert color_manager.color_indices == {"0xff0000": 0}
    assert len(color_manager.color_indices) == 1

    assert ochre.RGB(1, 0, 0) in color_manager
    assert len(color_manager) == 1

    color_manager.discard(ochre.Hex("#ff0000"))

    assert list(color_manager.colors) == []

    assert color_manager.color_indices == {}
    assert len(color_manager.color_indices) == 0

    assert ochre.RGB(1, 0, 0) not in color_manager
    assert len(color_manager) == 0
