"""Utilities for managing colors and color pairs in curses."""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Iterable, Iterator, Mapping, MutableSet, Optional, Union

import ochre


@dataclass
class ColorManager(
    Mapping[Union[Optional[ochre.Color], ochre.ColorPair], int],
    MutableSet[Union[Optional[ochre.Color], ochre.ColorPair]],
):
    """A class for managing curses colors and color pairs."""

    color_indices: dict[ochre.Color, int] = field(default_factory=lambda: {None: -1})
    next_color_index = 0

    pair_indices: dict[ochre.ColorPair, int] = field(default_factory=dict)
    next_pair_index = 0

    on_add_color: Optional[Callable[[ochre.Color, ColorManager], None]] = None
    on_add_pair: Optional[Callable[[ochre.ColorPair, ColorManager], None]] = None

    current_pair: ochre.ColorPair = ochre.ColorPair()

    @property
    def foreground(self) -> ochre.Color:
        """Return the current foreground color."""
        return self.current_pair.foreground

    @foreground.setter
    def foreground(self, color: ochre.Color) -> None:
        """Set the current foreground color."""
        self.current_pair = ochre.ColorPair(
            foreground=color, background=self.background
        )
        self.add_color(color)
        self.add_pair(self.current_pair)

    @property
    def background(self) -> ochre.Color:
        """Return the current background color."""
        return self.current_pair.background

    @background.setter
    def background(self, color: ochre.Color) -> None:
        """Set the current background color."""
        self.current_pair = ochre.ColorPair(
            foreground=self.foreground, background=color
        )
        self.add_color(color)
        self.add_pair(self.current_pair)

    @property
    def colors(self) -> Iterator[ochre.Color]:
        """Return all colors currently registered."""
        return map(
            lambda c: ochre.Hex(c) if c is not None else None, self.color_indices.keys()
        )

    @property
    def pairs(self) -> Iterable[ochre.ColorPair]:
        """Return all color pairs currently registered."""
        return self.pair_indices.keys()

    def add_color(self, color: Optional[ochre.Color], callback: bool = True) -> None:
        """Register a color with the color manager."""
        if color in self.color_indices:
            return

        self.color_indices[color] = self.next_color_index
        self.next_color_index += 1
        if callback and self.on_add_color:
            self.on_add_color(color, self)

    def add_pair(
        self, pair: ochre.ColorPair, callback: bool = True, allow_zero: bool = False
    ) -> None:
        """Register a color pair with the color manager."""
        # We want background to be added first because curses tends to use the
        # first (zeroth) color as the "unknown" color, and it is usually black.
        self.add_color(pair.background, callback=callback)
        self.add_color(pair.foreground, callback=callback)

        if pair in self.pair_indices:
            return

        if not allow_zero and self.next_pair_index == 0:
            raise RuntimeError("Cannot redefine color pair 0")

        self.pair_indices[pair] = self.next_pair_index
        self.next_pair_index += 1
        if callback and self.on_add_pair:
            self.on_add_pair(pair, self)

    def discard_color(self, color: Optional[ochre.Color]) -> None:
        """Unregister a color from the color manager."""
        if color not in self.color_indices:
            return

        del self.color_indices[color]

    def discard_pair(self, pair: ochre.ColorPair) -> None:
        """Unregister a color pair from the color manager."""
        if pair not in self.pair_indices:
            return

        del self.pair_indices[pair]

    def add(
        self, value: Optional[ochre.Color | ochre.ColorPair], allow_zero: bool = False
    ) -> None:
        """Register a color or color pair with the color manager."""
        if value is None or isinstance(value, ochre.Color):
            return self.add_color(value)

        if isinstance(value, ochre.ColorPair):
            return self.add_pair(value, allow_zero=allow_zero)

        raise TypeError(f"Unsupported type: {type(value)}")

    def discard(self, value: Optional[ochre.Color | ochre.ColorPair]) -> None:
        """Unregister a color or color pair from the color manager."""
        if value is None or isinstance(value, ochre.Color):
            return self.discard_color(value)

        if isinstance(value, ochre.ColorPair):
            return self.discard_pair(value)

        raise TypeError(f"Unsupported type: {type(value)}")

    def __getitem__(self, value: Optional[ochre.Color | ochre.ColorPair]) -> int:
        """Return the index of a color or color pair."""
        if value is None or isinstance(value, ochre.Color):
            return self.color_indices[value]

        if isinstance(value, ochre.ColorPair):
            return self.pair_indices[value]

        raise TypeError(f"Unsupported type: {type(value)}")

    def __iter__(self) -> Iterator[ochre.Color]:
        """Return an iterator over all colors currently registered."""
        return self.colors

    def __len__(self) -> int:
        """Return the number of colors currently registered."""
        return len(self.color_indices)
