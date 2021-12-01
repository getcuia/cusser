"""A curses wrapper that understands ANSI escape code sequences."""


from __future__ import annotations

import curses
from dataclasses import dataclass
from typing import Text

import ochre
from stransi import Ansi, SetAttribute, SetClear, SetColor, SetCursor
from stransi.attribute import Attribute
from stransi.clear import Clear
from stransi.color import ColorRole
from stransi.cursor import CursorMove

from .color_manager import ColorManager, ColorPair

__version__ = "0.1.0"


__all__ = ["Cusser"]


def on_add_color(color: ochre.Color, manager: ColorManager) -> None:
    """Initialize a color when it is added to the color manager."""
    color = color.rgb
    return curses.init_color(
        manager[color],
        int(1000 * color.red),
        int(1000 * color.green),
        int(1000 * color.blue),
    )


def on_add_pair(pair: ColorPair, manager: ColorManager) -> None:
    """Initialize a color pair when it is added to the color manager."""
    curses.init_pair(manager[pair], manager[pair.foreground], manager[pair.background])


@dataclass
class Cusser:
    """A curses wrapper that understands ANSI escape code sequences."""

    window: curses._CursesWindow
    color_manager: ColorManager = ColorManager(
        on_add_color=on_add_color, on_add_pair=on_add_pair
    )

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

    def __post_init__(self):
        """
        Initialize the color manager.

        We assume the terminal actually supports colors.
        """
        curses.start_color()
        curses.use_default_colors()

        # We have to define the zero color pair here, otherwise we'll get a nasty
        # error later.
        self.color_manager.add_pair(
            ColorPair(ochre.WebColor("white"), ochre.WebColor("black")), allow_zero=True
        )

    def addstr(self, text: Text) -> None:
        """Add a string to the window, interpreting ANSI escape codes."""
        for instruction in Ansi(text).instructions():
            if isinstance(instruction, Text):
                self.window.addstr(instruction)
            elif isinstance(instruction, SetAttribute):
                self._set_attribute(instruction.attribute)
            elif isinstance(instruction, SetColor):
                self._set_color(instruction.role, instruction.color)
            elif isinstance(instruction, SetClear):
                self._set_clear(instruction.region)
            elif isinstance(instruction, SetCursor):
                self._set_cursor(instruction.move)
            else:
                raise NotImplementedError(instruction)

    def _set_attribute(self, attribute: Attribute) -> None:
        """Set the current attribute."""
        if attribute in self._ON_ATTR_MAP:
            if attribute == Attribute.NORMAL:
                self._set_color(ColorRole.FOREGROUND, None)
                self._set_color(ColorRole.BACKGROUND, None)
            return self.window.attron(self._ON_ATTR_MAP[attribute])

        if attribute in self._OFF_ATTR_MAP:
            return self.window.attroff(self._OFF_ATTR_MAP[attribute])

        raise ValueError(f"Unsupported attribute: {attribute}")

    def _set_color(self, role: ColorRole, color: ochre.Color) -> None:
        """Set the current color."""
        if role == ColorRole.FOREGROUND:
            self.color_manager.foreground = color
        elif role == ColorRole.BACKGROUND:
            self.color_manager.background = color
        else:
            raise ValueError(f"Unknown color role {role}")

        self.window.attron(
            curses.color_pair(self.color_manager[self.color_manager.current_pair])
        )

    def _set_clear(self, region: Clear) -> None:
        """Set the current clear region."""
        if region == Clear.SCREEN:
            return self.window.erase()

        if region == Clear.SCREEN_AFTER:
            return self.window.clrtobot()

        if region == Clear.LINE:
            # https://stackoverflow.com/a/20311594/4039050
            y, x = self.window.getyx()
            self.window.move(y, 0)
            return self.window.clrtoeol()
            # self.window.move(y, x)

        if region == Clear.LINE_AFTER:
            return self.window.clrtoeol()

        raise ValueError(f"Unsupported clear region {region}")

    def _set_cursor(self, move: CursorMove) -> None:
        """Set the current cursor position."""
        if not move.relative:
            y, x = move.y, move.x
        else:
            y, x = self.window.getyx()
            y += move.y
            x += move.x
        self.window.move(y, x)

    def __getattr__(self, name):
        """Forward all other calls to the underlying window."""
        return getattr(self.window, name)
