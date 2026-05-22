from pacman.game.Maze import Maze
from pacman.entities.Player import Player


class GameWorld:
    def __init__(self) -> None:
        self.__maze = Maze((18, 18))
        print(f'MAAAAAZE: {self.__maze}')
        self.__player = Player()
        self.__ghosts = None

    @property
    def maze(self):
        return self.__maze

    @maze.setter
    def _maze(self, value):
        self.__maze = value

    @property
    def player(self):
        return self.__player

    @player.setter
    def _player(self, value):
        self.__player = value

    @property
    def ghosts(self):
        return self.__ghosts

    @ghosts.setter
    def _ghosts(self, value):
        self.__ghosts = value
