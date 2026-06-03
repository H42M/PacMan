from pacman.entities.Player import Player
from pacman.game.Maze import Maze
from pacman.game.ai.ChaseAI import ChaseAI
from pacman.game.ai.algo.A_Star import A_Star


class ShyChase(ChaseAI):
    def __init__(self) -> None:
        super().__init__()
        self.__chase_target = 'player'

    def get_next_pos(self, ghost_pos: tuple[int, int],
                     player: Player,
                     maze: Maze) -> tuple[int, int]:
        astar_player = A_Star()
        soluce_player = astar_player.solve(ghost_pos, player.pos, maze)
        if len(soluce_player) < 8 or self.__chase_target == 'corner':
            corner_pos = (0, maze.h - 1)
            if ghost_pos != corner_pos:
                self.__chase_target = 'corner'
                a_star_far = A_Star()
                soluce_far = a_star_far.solve(ghost_pos, corner_pos, maze)
                return soluce_far[1]
        self.__chase_target = 'player'
        return soluce_player[1] if len(soluce_player) > 1 else ghost_pos
