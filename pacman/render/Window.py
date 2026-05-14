from pacman.render.Container import Container
from pacman.render.Screen import Screen
from typing import Optional
from pacman.render.interactives.Button import Button
import pygame


class Window(Container):
    def __init__(self, screen: Screen,
                 way: str,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 gap: int = 0,
                 padding: int = 0,
                 bg_color: Optional[tuple[int, int, int]] = None,
                 display_default: bool = False,
                 ) -> None:
        super().__init__(screen, way, pos, size, gap, padding)
        self.__bg_color = bg_color
        self.__display = display_default
        self.__cross_btn = Button(self._screen, 'X',
                                  callback=self.switch_display)

    def render(self) -> None:
        if not self.__display:
            return

        if self._pos and self._size:
            pygame.draw.rect(
                # window,
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
            end_window = (self._pos[0] + self._size[0],
                          self._pos[1] + self._size[1])
            cross_size = (50, 40)
            self.__cross_btn.size = cross_size
            self.__cross_btn.pos = (end_window[0] - cross_size[0],
                                    self._pos[1])
            self.__cross_btn.render()
        super().render()

    def switch_display(self) -> None:
        self.display = not self.display

    @property
    def display(self) -> bool:
        return self.__display

    @display.setter
    def display(self, value: bool) -> None:
        self.__display = value
        if self.__display:
            self._screen.record_clickable(self.__cross_btn)
        else:
            self._screen.delete_clickable(self.__cross_btn)
