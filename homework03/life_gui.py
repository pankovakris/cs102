import pygame
from pygame.locals import *

from ui import UI
from life import GameOfLife


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 30, speed: int = 10) -> None:
        self.grid = life.curr_generation
        self.cell_size = cell_size
        self.width = self.life.rows * self.cell_size
        self.height = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            j * self.cell_size,
                            i * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            j * self.cell_size,
                            i * self.cell_size,
                            self.cell_size,
                            self.cell_size,
                        ),
                    )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.life.create_grid(randomize=True)

        pause = False
        running = True
        while (
            running
            and (self.life.is_max_generations_exceeded is False)
            and (self.life.is_changing is True)
        ):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    pause = not pause
                elif event.type == pygame.MOUSEBUTTONUP:
                    i, j = event.pos
                    i = i // self.cell_size
                    j = j // self.cell_size
                    if self.life.curr_generation[j][i] == 0:
                        self.life.curr_generation[j][i] = 1
                    else:
                        self.life.curr_generation[j][i] = 0
                    self.draw_grid()
                    pygame.display.flip()
            if pause:
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                continue
            self.draw_grid()
            self.draw_lines()
            self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
