from pacman.game.Maze import Maze
from pacman.entities.Player import Player
from pacman.entities.Ghost import Ghost
from pacman.game.ai import VectorChase, ShyChase, AmbushChase, DirectChase


class GameWorld:
    def __init__(self) -> None:
        self.__maze = Maze((14, 14))
        self.__player = Player()

        blinky = Ghost((13, 13), DirectChase())
        pinky = Ghost((12, 13), AmbushChase())
        clyde = Ghost((11, 13), ShyChase())
        inky = Ghost((10, 13), VectorChase(blinky))

        self.__ghosts = [blinky, pinky, clyde, inky]

    @property
    def maze(self) -> Maze:
        return self.__maze

    @maze.setter
    def maze(self, value: Maze) -> None:
        self.__maze = value

    @property
    def player(self) -> Player:
        return self.__player

    @player.setter
    def player(self, value: Player) -> None:
        self.__player = value

    @property
    def ghosts(self) -> list[Ghost]:
        return self.__ghosts

    @ghosts.setter
    def ghosts(self, value: list[Ghost]) -> None:
        self.__ghosts = value
