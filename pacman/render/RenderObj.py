import pygame
from typing import Optional
from pacman.render.Screen import Screen


class RenderOBJ:

    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None) -> None:
        self._screen = screen

        self._surface: Optional[pygame.Surface] = None
        self._pos: Optional[tuple[int, int]] = pos
        self._size: Optional[tuple[int, int]] = size

    def render(self) -> None:
        pass

    # Getters / Setters

    @property
    def surface(self) -> Optional[pygame.Surface]:
        return self._surface

    @surface.setter
    def surface(self, value: pygame.Surface) -> None:
        self._surface = value

    @property
    def size(self) -> Optional[tuple[int, int]]:
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        if value:
            self._size = value

    @property
    def w(self) -> Optional[int]:
        if self._size:
            return self._size[0]
        return None

    @w.setter
    def w(self, value: Optional[int]) -> None:
        if value:
            if self._size:
                self._size = (value, self._size[1])
            else:
                self._size = (value, 0)

    @property
    def h(self) -> Optional[int]:
        if self._size:
            return self._size[1]
        return None

    @h.setter
    def h(self, value: Optional[int]) -> None:
        if value:
            if self._size:
                self._size = (self._size[0], value)
            else:
                self._size = (0, value)

    @property
    def pos(self) -> Optional[tuple[int, int]]:
        return self._pos

    @pos.setter
    def pos(self, value: Optional[tuple[int, int]]) -> None:
        if value:
            self._pos = value

    @property
    def x(self) -> Optional[int]:
        if self._pos:
            return self._pos[0]
        return None

    @x.setter
    def x(self, value: Optional[int]) -> None:
        if value:
            if self._pos:
                self._pos = (value, self._pos[1])
            else:
                self._pos = (value, 0)

    @property
    def y(self) -> Optional[int]:
        if self._pos:
            return self._pos[1]
        return None

    @y.setter
    def y(self, value: Optional[int]) -> None:
        if value:
            if self._pos:
                self._pos = (self._pos[0], value)
            else:
                self._pos = (0, value)
