import pygame
from typing import Optional
from pacman.render.Screen import Screen
from abc import ABC, abstractmethod


class RenderOBJ(ABC):
    """Define shared behavior for renderable objects."""

    def __init__(self, screen: Screen,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None) -> None:
        """Initialize RenderObj."""
        self._screen = screen

        self._surface: Optional[pygame.Surface] = None
        self._pos: Optional[tuple[int, int]] = pos
        self._size: Optional[tuple[int, int]] = size

    @abstractmethod
    def render(self) -> None:
        """Display objetc on screen."""
        pass

    # Getters / Setters

    @property
    def surface(self) -> Optional[pygame.Surface]:
        """Return the render surface."""
        return self._surface

    @surface.setter
    def surface(self, value: pygame.Surface) -> None:
        """Set the render surface."""
        self._surface = value

    @property
    def size(self) -> Optional[tuple[int, int]]:
        """Return the render object size."""
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        """Set the render object size."""
        if value is not None:
            self._size = value

    @property
    def w(self) -> Optional[int]:
        """Return the render object width."""
        if self._size:
            return self._size[0]
        return None

    @w.setter
    def w(self, value: Optional[int]) -> None:
        """Set the render object width."""
        if value is not None:
            if self._size:
                self._size = (value, self._size[1])
            else:
                self._size = (value, 0)

    @property
    def h(self) -> Optional[int]:
        """Return the render object height."""
        if self._size is not None:
            return self._size[1]
        return None

    @h.setter
    def h(self, value: Optional[int]) -> None:
        """Set the render object height."""
        if value is not None:
            if self._size:
                self._size = (self._size[0], value)
            else:
                self._size = (0, value)

    @property
    def pos(self) -> Optional[tuple[int, int]]:
        """Return the render object position."""
        return self._pos

    @pos.setter
    def pos(self, value: Optional[tuple[int, int]]) -> None:
        """Set the render object position."""
        if value is not None:
            self._pos = value

    @property
    def x(self) -> Optional[int]:
        """Return the render object x position."""
        if self._pos is not None:
            return self._pos[0]
        return None

    @x.setter
    def x(self, value: Optional[int]) -> None:
        """Set the render object x position."""
        if value is not None:
            if self._pos:
                self._pos = (value, self._pos[1])
            else:
                self._pos = (value, 0)

    @property
    def y(self) -> Optional[int]:
        """Return the render object y position."""
        if self._pos is not None:
            return self._pos[1]
        return None

    @y.setter
    def y(self, value: Optional[int]) -> None:
        """Set the render object y position."""
        if value is not None:
            if self._pos:
                self._pos = (self._pos[0], value)
            else:
                self._pos = (0, value)
