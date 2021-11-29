"""Utilities for managing colors and color pairs in curses."""


from dataclasses import dataclass, field
from typing import Iterable, Optional

import ochre


@dataclass
class ColorPair:
    """A color pair of foreground and background colors."""

    # TODO: move this to ochre
    foreground: Optional[ochre.Color] = None
    background: Optional[ochre.Color] = None


@dataclass
class ColorManager:
    """A class for managing curses colors and color pairs."""

    color_indices: dict[ochre.Color, int] = field(default_factory=dict)
    next_index = 0

    def add(self, color: ochre.Color) -> None:
        """Register a color with the color manager."""
        h = hex(color)
        if h not in self.color_indices:
            self.color_indices[h] = self.next_index
            self.next_index += 1

    def discard(self, color: ochre.Color) -> None:
        """Unregister a color from the color manager."""
        h = hex(color)
        if h in self.color_indices:
            del self.color_indices[h]

    @property
    def colors(self) -> Iterable[ochre.Color]:
        """Return all colors currently registered."""
        return map(ochre.Hex, self.color_indices.keys())

    def __len__(self) -> int:
        """Return the number of colors currently registered."""
        return len(self.color_indices)

    def __iter__(self) -> Iterable[ochre.Color]:
        """Return an iterator over all colors currently registered."""
        return self.colors
