import curses
from math import floor
from pyTermUI.ui import UI
from pyTermUI.region import Region
from pyTermUI.position import Position
from pyTermUI.text import Text


def main(stdscr):
    def on_click(text):
        ...

    ui = UI(stdscr)

    region = Region("Test", Position.ORIGIN(), Position.DEFAULT_TERM_SIZE())
    region.framed = True

    cellwidth = 18
    cellheight = 6

    cells = []

    board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    vertical = "│"
    horizontal = "─"
    cross = "┼"

    boardx = cellwidth * 2 + 2
    boardy = cellheight * 2 + 2

    for y in range(boardy):
        for x in range(boardx):
            if x % (cellwidth + 1) == 0:
                region.add_element(
                    Text(
                        vertical,
                        Position(
                            region.size.half().x - floor(cellwidth / 2) - 2 + x,
                            region.size.half().y - y + 1,
                        ),
                    )
                )

            if y % (cellheight + 1) == 0:
                text = horizontal * (boardx + cellwidth)
                new = []

                for i, char in enumerate(text):
                    new.append(char)
                    if (i + 1) % (cellwidth + 1) == 0:
                        new[i] = cross

                new = "".join(text)

                region.add_element(
                    Text(
                        new,
                        Position(
                            region.size.half().x - floor(len(text) / 2) - 1,
                            region.size.half().y - y + 1,
                        ),
                    )
                )

    ui.add_region(region)

    ui.activate()


if __name__ == "__main__":
    curses.wrapper(main)
