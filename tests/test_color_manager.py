"""Tests for the color manager class."""

from typing import Optional

import ochre
import pytest

from cusser.color_manager import ColorManager, ColorPair


@pytest.fixture
def color_manager() -> ColorManager:
    """Return a new ColorManager."""
    color_manager = ColorManager()
    color_manager.add(
        ColorPair(ochre.WebColor("white"), ochre.WebColor("black")), allow_zero=True
    )
    color_manager.add(ColorPair(ochre.WebColor("blue"), ochre.WebColor("black")))
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

    # assert list(color_manager.colors) == [ochre.RGB(1, 0, 0)]

    assert color_manager.color_indices == {None: -1, "0xff0000": n}
    assert len(color_manager.color_indices) == 2

    assert ochre.RGB(1, 0, 0) in color_manager
    assert len(color_manager) == 2

    color_manager.discard(ochre.Hex("#ff0000"))

    assert list(color_manager.colors) == [None]

    assert color_manager.color_indices == {None: -1}
    assert len(color_manager.color_indices) == 1

    assert ochre.RGB(1, 0, 0) not in color_manager
    assert len(color_manager) == 1


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
    assert len(color_manager) == 5

    color_manager.discard(ColorPair(ochre.Hex("#ff0000"), ochre.Hex("#000000")))

    assert not list(color_manager.pairs)

    assert color_manager.pair_indices == {}
    assert len(color_manager.pair_indices) == 0

    assert ColorPair(ochre.Hex("#ff0000"), ochre.Hex("#000000")) not in color_manager
    assert len(color_manager) == 5


def test_callbacks(color_manager: ColorManager):
    """Test callbacks for color and pair additions."""
    last_color: Optional[ochre.Color] = None
    last_pair: Optional[ColorPair] = None

    color_manager.add(ochre.WebColor("violet"))
    color_manager.add(ColorPair(ochre.WebColor("beige"), ochre.WebColor("lavender")))
    assert last_color is None
    assert last_pair is None

    def color_callback(color: ochre.Color, manager: ColorManager) -> None:
        nonlocal last_color
        last_color = color
        print(f"color_callback: {color} has index {manager[color]}")

    def pair_callback(pair: ColorPair, manager: ColorManager) -> None:
        nonlocal last_pair
        last_pair = pair
        print(f"pair_callback: {pair} has index {manager[pair]}")

    color_manager.on_add_color = color_callback
    color_manager.on_add_pair = pair_callback

    color_manager.add(ochre.WebColor("snow"))
    assert last_color == ochre.WebColor("snow")

    color_manager.add(ColorPair(ochre.WebColor("teal"), ochre.WebColor("gold")))
    assert last_color == ochre.WebColor("teal")  # foregrounds are added last
    assert last_pair == ColorPair(ochre.WebColor("teal"), ochre.WebColor("gold"))


def test_managing_defaults(color_manager: ColorManager):
    """Test managing default color and pair."""
    assert None in color_manager

    color_manager.add(None)
    color_manager.add(ColorPair())

    assert None in color_manager
    assert ColorPair() in color_manager

    color_manager.discard(None)
    color_manager.discard(ColorPair())

    # assert None in color_manager
    # assert ColorPair() in color_manager


def test_managing_current_pair(color_manager: ColorManager):
    """Test managing the current pair."""
    assert color_manager.foreground is None
    assert color_manager.background is None

    color_manager.foreground = ochre.RGB(0, 0, 0.5)
    assert color_manager.foreground == ochre.RGB(0, 0, 0.5)
    assert color_manager.background is None
    assert ochre.RGB(0, 0, 0.5) in color_manager

    color_manager.background = ochre.WebColor("black")
    assert color_manager.foreground == ochre.RGB(0, 0, 0.5)
    assert color_manager.background == ochre.RGB(0, 0, 0)
    assert ochre.Hex("#000000") in color_manager

    color_manager.foreground = ochre.RGB(1, 1, 1)
    color_manager.background = ochre.RGB(0, 0, 0)
    assert color_manager.foreground == ochre.Hex("#ffffff")
    assert color_manager.background == ochre.Hex("#000000")
    assert ochre.Hex("#ffffff") in color_manager
    assert ochre.Hex("#000000") in color_manager

    color_manager.foreground = None
    color_manager.background = None
    assert color_manager.foreground is None
    assert color_manager.background is None
    assert None in color_manager
