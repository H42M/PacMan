from pacman.entities.Player import Player
from pacman.game.Maze import Maze
from pacman.game.ai.ChaseAI import ChaseAI
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pacman.entities.Ghost import Ghost
from pacman.game.ai.algo.A_Star import A_Star


class VectorChase(ChaseAI):
    def __init__(self, vector_ghost: 'Ghost') -> None:
        super().__init__()
        self.__vector_ghost = vector_ghost

    def get_next_pos(self, ghost_pos: tuple[int, int], player: Player,
                     maze: Maze) -> tuple[int, int]:

        map_dir = {
            'n': (0, -1),
            's': (0, 1),
            'e': (1, 0),
            'w': (-1, 0)
        }

        dx, dy = map_dir[player.dir_str.lower()]

        target1 = (
            player.pos[0] + (dx * 2),
            player.pos[1] + (dy * 2)
        )

        bx, by = self.__vector_ghost.pos

        target = (
            max(0, min(maze.w - 1, 2 * target1[0] - bx)),
            max(0, min(maze.h - 1, 2 * target1[1] - by))
        )

        astar = A_Star()
        soluce = astar.solve(ghost_pos, target, maze)

        return soluce[1] if len(soluce) > 1 else ghost_pos
