from pacman.player import PlayerState
from pacman.maze_adapter import GeneratedMaze
from pacman.entities.ai.ChaseAI import ChaseAI
from pacman.entities.ai.algo.A_Star import A_Star

# from typing import TYPE_CHECKING
# if TYPE_CHECKING:
#     from pacman.entities.Ghost import Ghost


class VectorChase(ChaseAI):
    def __init__(self, vector_ghost: Ghost) -> None:
        super().__init__()
        self.__vector_ghost = vector_ghost

    def get_next_pos(self, ghost_pos: tuple[int, int], player: PlayerState,
                     maze: GeneratedMaze) -> tuple[int, int]:

        map_dir = {
            'n': (0, -1),
            's': (0, 1),
            'e': (1, 0),
            'w': (-1, 0)
        }

        dx, dy = map_dir[player.dir_str.lower()]

        target1 = (
            player.position[0] + (dx * 2),
            player.position[1] + (dy * 2)
        )

        bx, by = self.__vector_ghost.pos

        target = (
            max(0, min(maze.width - 1, 2 * target1[0] - bx)),
            max(0, min(maze.height - 1, 2 * target1[1] - by))
        )

        astar = A_Star()
        soluce = astar.solve(ghost_pos, target, maze)

        return soluce[1] if len(soluce) > 1 else ghost_pos
