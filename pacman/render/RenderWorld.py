from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Entity import RenderEntity

from pacman.game.GameWorld import GameWorld

from typing import Optional


class RenderWorld(RenderOBJ):
    def __init__(self, screen: Screen,
                 world: GameWorld,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 ) -> None:
        super().__init__(screen, pos, size)
        self.__world = world
        self.__render_maze = RenderMaze(screen, world.maze)
        self.__render_player = RenderEntity(screen, world.player)

    def render(self) -> None:
        self.__render_maze.render()
        self.__render_player.render()