from abc import abstractmethod, ABC
from pacman.game.Maze import Maze
from collections import deque
from pacman.entities.Player import Player


class ChaseAI(ABC):
    def __init__(self) -> None:
        self._chase_history = deque(maxlen=10)

    @abstractmethod
    def get_next_pos(self, ghost_pos: tuple[int, int],
                     player: Player, maze: Maze
                     ) -> tuple[int, int]:
        pass
