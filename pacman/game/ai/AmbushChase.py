from pacman.entities.Player import Player
from pacman.game.Maze import Maze
from pacman.game.ai.ChaseAI import ChaseAI


class AmbushChase(ChaseAI):
    def __init__(self) -> None:
        super().__init__()

    def get_next_pos(self, ghost_pos: tuple[int, int],
                     player: Player, maze: Maze
                     ) -> tuple[int, int]:

        self._chase_history.append(ghost_pos)
        av_dir = self._get_av_dir(ghost_pos, maze)
        difficulty = 'HARD'

        px, py = player.pos
        d = player.dir_str.upper()

        if d == 'N':
            target = (px, max(0, py - 4))
        elif d == 'S':
            target = (px, min(maze.h - 1, py + 4))
        elif d == 'E':
            target = (min(maze.w - 1, px + 4), py)
        elif d == 'W':
            target = (max(0, px - 4), py)
        else:
            target = player.pos

        if difficulty == 'EASY':
            return self._get_best_dir(ghost_pos, target, av_dir)
        else:
            from pacman.game.ai.algo.A_Star import A_Star

            astar = A_Star()
            soluce = astar.solve(ghost_pos, target, maze)
            return soluce[1] if len(soluce) > 1 else ghost_pos
