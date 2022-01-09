import curses
from time import sleep

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        for y, row in enumerate(self.life.curr_generation):
            for x, cell in enumerate(row):
                if cell == 1:
                    char = "*"
                else:
                    char = " "
                screen.addch(y + 1, x + 1, char)

    def run(self) -> None:
        screen = curses.initscr()
        curses.resize_term(self.life.rows + 2, self.life.cols + 2)
        while self.life.is_changing and not self.life.is_max_generations_exceeded:
            self.life.step()
            self.draw_borders(screen)
            self.draw_grid(screen)
            screen.refresh()
            sleep(1)
        screen.refresh()
        curses.endwin()


if __name__ == '__main__':
	life = GameOfLife((24, 80), max_generations=50)
	con = Console(life)
	con.run()
