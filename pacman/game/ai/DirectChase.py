from pacman.game.ai.ChaseAI import ChaseAI
from pacman.game.Maze import Maze


class DirectChase(ChaseAI):

    def __init__(self) -> None:
        super().__init__()

    def get_next_pos(self, ghost_pos: tuple[int, int],
                     player_pos: tuple[int, int], maze: Maze
                     ) -> tuple[int, int]:
        self._chase_history.append(ghost_pos)
        if ghost_pos == player_pos:
            return ghost_pos

        av_dir = self.__get_av_dir(ghost_pos, maze)
        best_dist = 100000.0
        best_pos = ghost_pos

        if len(av_dir) == 1:
            return av_dir[0]

        for neighbor in av_dir:
            dist = abs(neighbor[0] - player_pos[0]) + \
                   abs(neighbor[1] - player_pos[1])

            last_pos = ghost_pos
            if len(self._chase_history) > 1:
                last_pos = self._chase_history[-2]

            if dist < best_dist and neighbor != last_pos:
                best_dist = dist
                best_pos = neighbor

        return best_pos

    def __get_av_dir(self, ghost_pos: tuple[int, int], maze: Maze
                     ) -> list[tuple[int, int]]:

        dir_map = {
            'n': [0, -1],
            's': [0, 1],
            'e': [1, 0],
            'w': [-1, 0]
        }
        av_pos = []
        for dir, move in dir_map.items():
            if not maze.get_cell_wall(ghost_pos, dir):
                new_pos = (ghost_pos[0] + move[0], ghost_pos[1] + move[1])
                av_pos.append(new_pos)
        return av_pos
