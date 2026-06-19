from typing import Optional, Union

import pygame

from pacman.render.Container import Container
from pacman.render.Screen import Screen
from pacman.render.interactives.Button import Button


class Window(Container):
    """Container with a close button and borders."""

    def __init__(
        self,
        screen: Screen,
        way: str,
        pos: Optional[tuple[int, int]] = None,
        size: Optional[tuple[int, int]] = None,
        gap: int = 0,
        padding: int = 0,
        bg_color: Optional[Union[tuple[int, int, int],
                                 tuple[int, int, int, int]]] = None,
        display_default: bool = False,
    ) -> None:
        """Initialize a bordered window container."""
        super().__init__(
            screen,
            way,
            pos,
            size,
            gap,
            padding,
            display=display_default,
        )
        self.__bg_color = bg_color
        self.__cross_btn = Button(
            self._screen,
            'X',
            callback=self.switch_display
        )
        if self.display:
            self._screen.record_clickable(self.__cross_btn)

    def render(self) -> None:
        """Display window and contained elements on screen."""
        if not self.display:
            return

        if self._pos and self._size:
            pygame.draw.rect(
                self._screen.screen,
                self.__bg_color if self.__bg_color else (0, 0, 0),
                (*self._pos, *self._size),
                border_radius=10
            )
            pygame.draw.rect(
                self._screen.screen,
                (255, 255, 255),
                (*self._pos, *self._size),
                width=2,
                border_radius=10
            )

            end_window = (
                self._pos[0] + self._size[0],
                self._pos[1] + self._size[1],
            )
            cross_size = (50, 40)
            self.__cross_btn.size = cross_size
            self.__cross_btn.pos = (
                end_window[0] - cross_size[0],
                self._pos[1],
            )
            self.__cross_btn.render()

        super().render()

    def switch_display(self) -> None:
        """Reverse the display state."""
        self.display = not self.display

    def _on_display_changed(self) -> None:
        """Synchronize the close button when visibility changes."""
        self.__sync_cross_button_clickable()

    def __sync_cross_button_clickable(self) -> None:
        """Register or remove the close button based on visibility."""
        if self.display:
            self._screen.record_clickable(self.__cross_btn)
        else:
            self._screen.delete_clickable(self.__cross_btn)
