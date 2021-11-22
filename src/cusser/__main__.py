"""Run a simple test of the Cusser class."""


import curses


from . import Cusser


if __name__ == "__main__":

    def _app(stdscr):
        stdscr = Cusser(stdscr)
        text = "\033[1;5;33mHello \033[2mWorld\033[0m!"
        stdscr.addstr(text)
        stdscr.refresh()
        stdscr.getch()

    curses.wrapper(_app)
