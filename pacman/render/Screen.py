
from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import pygame
from pacman.render.RenderConfig import RenderConfig

if TYPE_CHECKING:
    from pacman.render.interactives.Button import Button


class Screen:
    """Manage screen, all pygame stuff, and player interactions."""
    def __init__(self) -> None:
        """Initialize Screen."""
        pygame.init()
        pygame.key.set_repeat(400, 40)
        try:
            self.__screen_size = RenderConfig.screen_size
            self.__screen_name = 'PACMAN'
            self.__screen = pygame.display.set_mode(
                self.__screen_size
            )
            self.__clock = pygame.time.Clock()
            pygame.display.set_caption(self.__screen_name)
            self.__background: Optional[pygame.Surface] = None
            self.__clickables: list[Button] = []
        except Exception as e:
            raise ValueError(f'Screen loading error: {e}')

    def clear(self) -> None:
        """Reset screen."""
        if self.__background:
            scaled = pygame.transform.scale(self.__background,
                                            self.__screen_size)
            pos_tuple = (0, 0)
            self.screen.blit(scaled, pos_tuple)
        else:
            self.__screen.fill((0, 0, 0))

    def flip(self) -> None:
        """Display all elements rendered on screen."""
        self.__clock.tick(60)
        pygame.display.flip()

    def record_clickable(self, obj: Button) -> None:
        """Add a clickable objet to the list"""
        if obj not in self.__clickables:
            self.__clickables.append(obj)

    def delete_clickable(self, obj: Button) -> None:
        """Remove a clickable object to the list"""
        if obj in self.__clickables:
            self.__clickables.remove(obj)

    def reset_clickables(self) -> None:
        """Remove all registered clickable objects."""
        self.__clickables = []

    # GETTERS / SETTERS

    @property
    def screen(self) -> pygame.Surface:
        """Return the pygame screen surface."""
        return self.__screen

    @screen.setter
    def screen(self, value: pygame.Surface) -> None:
        """Set the pygame screen surface."""
        self.__screen = value

    @property
    def clickables(self) -> list[Button]:
        """Return registered clickable objects."""
        return self.__clickables

    @property
    def background(self) -> Optional[pygame.Surface]:
        """Return the screen background surface."""
        return self.__background

    @background.setter
    def background(self, value: pygame.Surface) -> None:
        """Set the screen background surface."""
        self.__background = value
