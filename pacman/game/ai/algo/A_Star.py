from typing import Any
import heapq
from pacman.game.Maze import Maze


class A_Star:
    """Find the shortest path through a maze."""

    def __init__(self) -> None:
        """Initialize the solver."""
        self.__traveled: list[tuple[int, int]] = []

    def solve(self, start: tuple[int, int], target: tuple[int, int],
              maze: Maze) -> list[tuple[int, int]]:
        """Return the shortest path from entry to exit."""
        counter = 0

        heap = [(self.__get_h(start, target), 0, counter, start, [start])]
        visited = set()

        while heap:
            f, g, _, cell, path = heapq.heappop(heap)

            if cell == target:
                return path
            if cell not in visited:
                visited.add(cell)

            for option in self.__get_av_options(cell, maze):
                neigh = option['neigh_cell']
                if neigh not in visited:
                    new_g = g + 1
                    new_f = new_g + self.__get_h(neigh, target)
                    counter += 1
                    heapq.heappush(heap, (new_f, new_g, counter,
                                          neigh, path + [neigh]))
        return []

    def __get_h(self, cell: tuple[int, int], target: tuple[int, int]) -> float:
        """Return the Manhattan distance to the exit."""
        return (abs(cell[0] - target[0]) +
                abs(cell[1] - target[1]))

    def __get_av_options(self, cell: tuple[int, int], maze: Maze) -> list[Any]:
        """Return available moves from a cell."""
        options = self.__get_options(cell)
        av_options = []
        for option in options:
            neigh: tuple[int, int] = option['neigh_cell']
            cell_wall: str = option['wall']

            if (not maze.get_cell_wall(cell, cell_wall) and
                    neigh not in self.__traveled):
                av_options.append(option)
        return av_options

    def __get_options(self, cell: tuple[int, int]
                      ) -> list[dict[str, Any]]:
        """Return adjacent cells and their shared walls."""
        return [
                {
                    'neigh_cell': (cell[0] - 1, cell[1]),
                    'cell': cell,
                    'wall': "w",
                    'neigh_wall': "e"
                 },
                {
                    'neigh_cell': (cell[0] + 1, cell[1]),
                    'cell': cell,
                    'wall': "e",
                    'neigh_wall': "w"
                 },
                {
                    'neigh_cell': (cell[0], cell[1] - 1),
                    'cell': cell,
                    'wall': "n",
                    'neigh_wall': "s"
                 },
                {
                    'neigh_cell': (cell[0], cell[1] + 1),
                    'cell': cell,
                    'wall': "s",
                    'neigh_wall': "n"
                 },
            ]
