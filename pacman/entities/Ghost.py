from pacman.entities.Character import Character
from pacman.entities.Player import Player
from pacman.game.Maze import Maze
from pacman.game.ai import ChaseAI, VectorChase, AmbushChase, DirectChase, \
    ShyChase
from typing import Optional


class Ghost(Character):
    DIRECT_CHASE = DirectChase
    AMBUSH_CHASE = AmbushChase
    VECTOR_CHASE = VectorChase
    SHY_CHASE = ShyChase

    def __init__(
        self,
        pos: tuple[int, int],
        chase_algo: "ChaseAI",
        vector_ghost: Optional['Ghost'] = None
    ) -> None:
        super().__init__(pos)

        self.__chase_algo = chase_algo
        self.__move_speed = 30
        self.__move_count = 0

    def move(self, player: Player, maze: Maze) -> None:
        self.__move_count += 1
        if self.__move_count >= self.__move_speed:
            self.pos = self.__chase_algo.get_next_pos(self.pos, player,
                                                      maze)
            self.__move_count = 0
