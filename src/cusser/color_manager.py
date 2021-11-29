"""Utilities for managing colors and color pairs in curses."""


from dataclasses import dataclass
from typing import Optional

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
