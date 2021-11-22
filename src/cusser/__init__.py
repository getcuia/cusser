"""A curses wrapper that understands ANSI escape code sequences."""


from __future__ import annotations

import curses
from dataclasses import dataclass
from typing import Text

from stransi import Ansi, SetAttribute
from stransi.attribute import Attribute

__version__ = "0.1.0"


__all__ = ["Cusser"]


@dataclass
class Cusser:
    """A curses wrapper that understands ANSI escape code sequences."""

    _ON_ATTR_MAP = {
        Attribute.NORMAL: curses.A_NORMAL,
        Attribute.BOLD: curses.A_BOLD,
        Attribute.DIM: curses.A_DIM,
        Attribute.ITALIC: curses.A_ITALIC,
        Attribute.UNDERLINE: curses.A_UNDERLINE,
        Attribute.BLINK: curses.A_BLINK,
        Attribute.REVERSE: curses.A_REVERSE,
        Attribute.HIDDEN: curses.A_INVIS,
    }

    _OFF_ATTR_MAP = {
        Attribute.NEITHER_BOLD_NOR_DIM: curses.A_BOLD | curses.A_DIM,
        Attribute.NOT_ITALIC: curses.A_ITALIC,
        Attribute.NOT_UNDERLINE: curses.A_UNDERLINE,
        Attribute.NOT_BLINK: curses.A_BLINK,
        Attribute.NOT_REVERSE: curses.A_REVERSE,
        Attribute.NOT_HIDDEN: curses.A_INVIS,
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
                if instruction.attribute in self._ON_ATTR_MAP:
                    self.window.attron(self._ON_ATTR_MAP[instruction.attribute])
                elif instruction.attribute in self._OFF_ATTR_MAP:
                    self.window.attroff(self._OFF_ATTR_MAP[instruction.attribute])
                else:
                    raise ValueError(f"Unknown attribute {instruction.attribute}")
            else:
                raise NotImplementedError(instruction)
