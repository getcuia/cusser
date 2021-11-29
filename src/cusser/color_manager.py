"""Utilities for managing colors and color pairs in curses."""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional, Text

import ochre


@dataclass
class ColorPair:
    """A color pair of foreground and background colors."""

    # TODO: move this to ochre
    foreground: Optional[ochre.Color] = None
    background: Optional[ochre.Color] = None

    @property
    def is_default(self) -> bool:
        """Return True if this color pair is the default."""
        return self.foreground is None or self.background is None


@dataclass
class ColorManager:
    """A class for managing curses colors and color pairs."""

    color_indices: dict[Text, int] = field(default_factory=dict)
    next_color_index = 0

    pair_indices: dict[tuple[Text, Text], int] = field(default_factory=dict)
    next_pair_index = 0

    def add(self, value: Optional[ochre.Color] | ColorPair) -> None:
        """Register a color or color pair with the color manager."""
        if value is None:
            return

        if isinstance(value, ochre.Color):
            self.add_color(value)
        elif isinstance(value, ColorPair):
            self.add_pair(value)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def add_color(self, color: Optional[ochre.Color]) -> None:
        """Register a color with the color manager."""
        if color is None:
            return

        c = hex(color)
        if c in self.color_indices:
            return

        self.color_indices[c] = self.next_color_index
        self.next_color_index += 1

    def add_pair(self, pair: ColorPair) -> None:
        """Register a color pair with the color manager."""
        if pair.is_default:
            return

        self.add_color(pair.foreground)
        self.add_color(pair.background)

        p = (hex(pair.foreground), hex(pair.background))
        if p in self.pair_indices:
            return

        self.pair_indices[p] = self.next_pair_index
        self.next_pair_index += 1

    def discard(self, value: Optional[ochre.Color] | ColorPair) -> None:
        """Unregister a color or color pair from the color manager."""
        if value is None:
            return

        if isinstance(value, ochre.Color):
            self.discard_color(value)
        elif isinstance(value, ColorPair):
            self.discard_pair(value)
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def discard_color(self, color: Optional[ochre.Color]) -> None:
        """Unregister a color from the color manager."""
        if color is None:
            return

        c = hex(color)
        if c not in self.color_indices:
            return

        del self.color_indices[c]

    def discard_pair(self, pair: ColorPair) -> None:
        """Unregister a color pair from the color manager."""
        if pair.is_default:
            return

        p = (hex(pair.foreground), hex(pair.background))
        if p not in self.pair_indices:
            return

        del self.pair_indices[p]

    @property
    def colors(self) -> Iterable[ochre.Color]:
        """Return all colors currently registered."""
        return map(ochre.Hex, self.color_indices.keys())

    @property
    def pairs(self) -> Iterable[ColorPair]:
        """Return all color pairs currently registered."""
        return map(
            lambda p: ColorPair(foreground=ochre.Hex(p[0]), background=ochre.Hex(p[1])),
            self.pair_indices.keys(),
        )

    def __iter__(self) -> Iterable[ochre.Color]:
        """Return an iterator over all colors currently registered."""
        return self.colors

    def __contains__(self, value: Optional[ochre.Color] | ColorPair) -> bool:
        """Return whether a color or color pair is registered."""
        if value is None:
            return True

        if isinstance(value, ochre.Color):
            return value in self.colors
        elif isinstance(value, ColorPair):
            if value.is_default:
                return True

            return value in self.pairs
        else:
            raise TypeError(f"Unsupported type: {type(value)}")

    def __len__(self) -> int:
        """Return the number of colors currently registered."""
        return len(self.color_indices)
