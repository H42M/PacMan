from pacman.game.ai.ChaseAI import ChaseAI
from pacman.game.Maze import Maze
from pacman.entities.Player import Player
from pacman.game.ai.algo.A_Star import A_Star


class DirectChase(ChaseAI):

    def __init__(self) -> None:
        super().__init__()

    def get_next_pos(self, ghost_pos: tuple[int, int],
                     player: Player, maze: Maze
                     ) -> tuple[int, int]:
        self._chase_history.append(ghost_pos)

        if ghost_pos == player.pos:
            return ghost_pos
        difficulty = 'HARD'
        # difficulty = 'EASY'

        if difficulty == 'EASY':
            av_dir = self._get_av_dir(ghost_pos, maze)
            best_pos = self._get_best_dir(ghost_pos, player.pos, av_dir)
        else:
            astar = A_Star()
            best_pos = astar.solve(ghost_pos, player.pos, maze)[1]

        return best_pos
