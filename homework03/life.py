import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, size, randomize: bool = True, max_generations: tp.Optional[int] = None
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0] * self.cols for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []
        for x, y in [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]:
            if 0 <= cell[0] + x < len(self.curr_generation) and 0 <= cell[1] + y < len(
                self.curr_generation[0]
            ):
                cells.append(self.curr_generation[cell[0] + x][cell[1] + y])
        return cells

    def get_next_generation(self) -> Grid:
        grid = deepcopy(self.curr_generation)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.curr_generation[i][j] == 1:
                    if (
                        sum(self.get_neighbours((i, j))) == 2
                        or sum(self.get_neighbours((i, j))) == 3
                    ):
                        grid[i][j] = 1
                    else:
                        grid[i][j] = 0
                else:
                    if sum(self.get_neighbours((i, j))) == 3:
                        grid[i][j] = 1
                    else:
                        grid[i][j] = 0
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is not None:
            return self.generations >= self.max_generations
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return not (self.curr_generation == self.prev_generation)

    @staticmethod
    def from_file(filename) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            line = f.readlines()
            game = GameOfLife((len(line), len(line[0].strip())), False)
            for i in range(len(line)):
                line[i].strip()
                for j in range(len(line[0].strip())):
                    game.curr_generation[i][j] = int(line[i][j])
        return game

    def save(self, filename) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join([str(chr) for chr in row]) + "\n")
        return
