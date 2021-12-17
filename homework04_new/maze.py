from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd
from numpy.lib.function_base import kaiser


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    if grid[coord[0]][coord[1]] != " ":
        grid[coord[0]][coord[1]] = " "
    elif coord[1] + 1 < len(grid[0]) - 1:
        grid[coord[0]][coord[1] + 1] = " "
    elif coord[0] - 1 > 1:
        grid[coord[0] - 1][coord[1]] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for j in range(1, rows - 1, 2):
        cor1 = j
        for i in range(1, cols - 1, 2):
            cor2 = i
            a = choice([-1, 1])
            if a == 1:
                if cor2 + 1 != cols - 1:
                    remove_wall(grid, (cor1, cor2 + 1))
                elif cor1 - 1 != 0:
                    remove_wall(grid, (cor1 - 1, cor2))
                else:
                    break
            else:
                if cor1 - 1 != 0:
                    remove_wall(grid, (cor1 - 1, cor2))
                elif cor2 + 1 != cols - 1:
                    remove_wall(grid, (cor1, cor2 + 1))
                else:
                    break

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    ans = []
    rows = len(grid) - 1
    columns = len(grid[0]) - 1

    for i in range(columns):
        if grid[0][i] == "X":
            ans.append((0, i))
    for j in range(rows):
        if grid[j][0] == "X":
            ans.append((j, 0))

    if len(ans) != 2:
        for i in range(columns):
            if grid[rows][i] == "X":
                ans.append((rows, i))
        for j in range(rows):
            if grid[j][columns] == "X":
                ans.append((j, columns))
    if len(ans) > 1:
        if ans[0][1] > ans[1][1]:
            ans[0], ans[1] = ans[1], ans[0]
        if ans[0][0] > ans[1][0]:
            ans[0], ans[1] = ans[1], ans[0]

    return ans


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    n = k + 1
    ways = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == k:
                for x, y in ways:
                    if 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]):
                        if grid[i + x][j + y] == 0:
                            grid[i + x][j + y] = n
    return grid


# return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    m = []
    cor1, cor2 = exit_coord[0], exit_coord[1]
    m.append((cor1, cor2))
    k = int(grid[cor1][cor2])
    ways = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    while grid[cor1][cor2] != 1:
        for x, y in ways:
            if 0 <= cor1 + x < len(grid) and 0 <= cor2 + y < len(grid[0]):
                if grid[cor1 + x][cor2 + y] != "■" and grid[cor1 + x][cor2 + y] != " ":
                    if grid[cor1 + x][cor2 + y] == k - 1:
                        cor1, cor2 = cor1 + x, cor2 + y
                        k -= 1
                        m.append((cor1, cor2))
    return m


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    if (
        coord == (0, 0)
        or coord == (len(grid) - 1, len(grid[0]) - 1)
        or coord == (len(grid) - 1, 0)
        or coord == (0, len(grid[0]) - 1)
    ):
        return True
    elif coord[0] == 0:
        if grid[1][coord[1]] != " ":
            return True

    elif coord[1] == 0:
        if grid[coord[0]][1] != " ":
            return True

    elif coord[0] == len(grid) - 1:
        if grid[len(grid) - 2][coord[1]] != " ":
            return True

    elif coord[1] == len(grid[0]) - 1:
        if grid[coord[0]][len(grid[0]) - 2] != " ":
            return True
    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, exits
    else:
        for exit in exits:
            if encircled_exit(grid, exit):
                return grid, None

    enter = exits[0]
    exit = exits[1]
    if exit[1] - enter[1] == 1 and exit[0] - enter[0] == 0:
        return grid, exits[::-1]
    elif exit[1] - enter[1] == 0 and exit[0] - enter[0] == 1:
        return grid, exits[::-1]
    elif exit[0] - enter[0] == 0 and exit[1] - enter[1] == 1:
        return grid, exits[::-1]
    elif exit[0] - enter[0] == 1 and exit[1] - enter[1] == 0:
        return grid, exits[::-1]

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == " ":
                grid[i][j] = 0

    grid[exits[0][0]][exits[0][1]] = 1
    grid[exits[1][0]][exits[1][1]] = 0

    k = 0
    while grid[exits[1][0]][exits[1][1]] == 0:
        k += 1
        make_step(grid, k)
    m = shortest_path(grid, exits[1])
    return grid, m


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
