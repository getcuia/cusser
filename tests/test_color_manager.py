"""Tests for the color manager class."""

import ochre
import pytest

from cusser.color_manager import ColorManager, ColorPair


@pytest.fixture
def color_manager() -> ColorManager:
    """Return a new ColorManager."""
    color_manager = ColorManager()
    color_manager.add(ColorPair(ochre.WebColor("blue"), ochre.WebColor("black")))
    color_manager.add(ColorPair(ochre.WebColor("white"), ochre.WebColor("black")))
    return color_manager


def test_color_management(color_manager: ColorManager):
    """Test adding, getting, and removing colors."""
    n = color_manager.next_color_index

    color_manager.discard(ochre.RGB(0, 0, 0))
    color_manager.discard(ochre.RGB(0, 0, 0))
    color_manager.discard(ochre.RGB(0, 0, 1))
    color_manager.discard(ochre.RGB(1, 1, 1))

    color_manager.add(ochre.Hex("#ff0000"))
    color_manager.add(ochre.Hex("#ff0000"))

    assert list(color_manager.colors) == [ochre.RGB(1, 0, 0)]

    assert color_manager.color_indices == {"0xff0000": n}
    assert len(color_manager.color_indices) == 1

    assert ochre.RGB(1, 0, 0) in color_manager
    assert len(color_manager) == 1

    color_manager.discard(ochre.Hex("#ff0000"))

    assert list(color_manager.colors) == []

    assert color_manager.color_indices == {}
    assert len(color_manager.color_indices) == 0

    assert ochre.RGB(1, 0, 0) not in color_manager
    assert len(color_manager) == 0


def test_pair_management(color_manager: ColorManager):
    """Test adding, getting, and removing color pairs."""
    n = color_manager.next_pair_index

    color_manager.discard(ColorPair(ochre.RGB(0, 0, 1), ochre.RGB(0, 0, 0)))
    color_manager.discard(ColorPair(ochre.RGB(0, 0, 1), ochre.RGB(0, 0, 0)))
    color_manager.discard(ColorPair(ochre.RGB(1, 1, 1), ochre.RGB(0, 0, 0)))

    color_manager.add(ColorPair(ochre.Hex("#ff0000"), ochre.Hex("#000000")))
    color_manager.add(ColorPair(ochre.Hex("#ff0000"), ochre.Hex("#000000")))

    assert list(color_manager.pairs) == [
        ColorPair(ochre.RGB(1, 0, 0), ochre.RGB(0, 0, 0))
    ]

    assert color_manager.pair_indices == {("0xff0000", "0x0"): n}
    assert len(color_manager.pair_indices) == 1

    assert ColorPair(ochre.Hex("#ff0000"), ochre.Hex("#000000")) in color_manager
    assert len(color_manager) == 4

    color_manager.discard(ColorPair(ochre.Hex("#ff0000"), ochre.Hex("#000000")))

    assert list(color_manager.pairs) == []

    assert color_manager.pair_indices == {}
    assert len(color_manager.pair_indices) == 0

    assert ColorPair(ochre.Hex("#ff0000"), ochre.Hex("#000000")) not in color_manager
    assert len(color_manager) == 4


def test_managing_defaults(color_manager: ColorManager):
    """Test managing default colors."""

    assert None in color_manager
    assert ColorPair(None, None) in color_manager

    color_manager.add(None)
    color_manager.add(ColorPair(None, None))

    assert None in color_manager
    assert ColorPair(None, None) in color_manager

    color_manager.discard(None)
    color_manager.discard(ColorPair(None, None))

    assert None in color_manager
    assert ColorPair(None, None) in color_manager
