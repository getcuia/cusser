"""A curses wrapper that understands ANSI escape code sequences."""


from __future__ import annotations

import curses
from dataclasses import dataclass

__version__ = "0.1.0"


__all__ = ["Cusser"]


@dataclass
class Cusser:
    """A curses wrapper that understands ANSI escape code sequences."""

    window: curses._CursesWindow

    def __getattr__(self, name):
        """Forward all other calls to the underlying window."""
        return getattr(self.window, name)
