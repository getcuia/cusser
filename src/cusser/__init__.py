"""A curses wrapper that understands ANSI escape code sequences."""


from __future__ import annotations

import curses
from dataclasses import dataclass
from typing import Text

from stransi import Ansi, SetAttribute, SetColor
from stransi.attribute import Attribute

__version__ = "0.1.0"


__all__ = ["Cusser"]


@dataclass
class Cusser:
    """A curses wrapper that understands ANSI escape code sequences."""

    ATTRIBUTE_MAP = {
        Attribute.BOLD: curses.A_BOLD,
        Attribute.DIM: curses.A_DIM,
        Attribute.BLINK: curses.A_BLINK,
        Attribute.NORMAL: curses.A_NORMAL,
    }

    window: curses._CursesWindow

    def __getattr__(self, name):
        """Forward all other calls to the underlying window."""
        return getattr(self.window, name)

    def addstr(self, text: Text) -> None:
        """Add a string to the window, interpreting ANSI escape codes."""
        for instruction in Ansi(text).instructions():
            if isinstance(instruction, Text):
                self.window.addstr(instruction)
            elif isinstance(instruction, SetAttribute):
                self.window.attron(self.ATTRIBUTE_MAP[instruction.attribute])
            elif isinstance(instruction, SetColor):
                pass
            else:
                raise NotImplementedError(instruction)
