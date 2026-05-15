from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen

from typing import Optional, Union
import pygame


class Container(RenderOBJ):
    """Container class.
    Used to automaticly set elements sizes and positions.
    Can be horizontal or vertical and can contain other container"""
    def __init__(self,
                 screen: Screen,
                 way: str,
                 pos: Optional[tuple[int, int]] = None,
                 size: Optional[tuple[int, int]] = None,
                 gap: int = 0,
                 padding: int = 0,
                 bg_color: Optional[Union[tuple[int, int, int],
                                          tuple[int, int, int, int]]] = None
                 ) -> None:
        """Initialize Container class"""
        super().__init__(screen, pos, size)
        self.__way = way
        self.__gap = gap
        self.__padding = padding
        self.__content: dict[RenderOBJ, int] = {}
        self._bg_color = bg_color
        self._gap_in_bg = True

    def __is_valid_percentage(self, value: str) -> bool:
        if not isinstance(value, str) or not value.endswith('%'):
            return False
        try:
            new_value = int(value[:-1])
        except ValueError:
            return False
        if not (0 <= new_value <= 100):
            return False
        return True

    def __are_all_elm_0(self) -> bool:
        for elm, size in self.__content.items():
            if size != 0:
                return False
        return True

    def add_content(self, objs: Union[dict[RenderOBJ, str],
                                      list[dict[RenderOBJ, str]]]
                    ) -> None:
        """Add element to container."""
        if isinstance(objs, dict):
            for key, value in objs.items():
                if not self.__is_valid_percentage(value):
                    raise ValueError(f"La valeur '{value}' n'est pas un "
                                     "pourcentage valide (format: '10%')")
                self.__content[key] = int(value[:-1])
        else:
            for item in objs:
                for key, value in item.items():
                    if not self.__is_valid_percentage(value):
                        raise ValueError(f"La valeur '{value}' n'est pas un "
                                         "pourcentage valide (format: '10%')")
                    self.__content[key] = int(value[:-1])
        if sum(size for _, size in self.__content.items()) > 100:
            raise ValueError("Sum of sizes is over 100% in container")
        self.__resize()

    def __resize(self) -> None:
        """Set size and pos for each contained elements"""
        if self._size and self._pos:
            available_width = self._size[0] - 2 * self.__padding
            available_height = self._size[1] - 2 * self.__padding

            nb_gap = len(self.__content) + 1
            total_gap = nb_gap * self.__gap

            if self.__way == "HORIZONTAL":
                end_x = self._pos[0] + self.__padding + self.__gap

                if self.__are_all_elm_0():
                    elm_size = ((available_width - total_gap) //
                                len(self.__content))
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.y = self._pos[1] + self.__padding
                        elm.w = elm_size
                        elm.x = end_x
                        elm.h = available_height
                        end_x = elm.x + elm_size + self.__gap
                        if isinstance(elm, Container):
                            elm.__resize()
                else:
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.y = self._pos[1] + self.__padding
                        elm.w = int(available_width * (size / 100))

                    if self.__gap == 0 and not self.__are_all_elm_0():
                        gap = self.__process_gap()
                    else:
                        gap = self.__gap

                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.x = end_x + gap
                        end_x = ((elm.x if elm.x else 0) +
                                 (elm.w if elm.w else 0))
                        if isinstance(elm, Container):
                            elm.__resize()

                        elm.h = available_height
            if self.__way == 'VERTICAL':
                end_y = self._pos[1] + self.__padding

                if self.__are_all_elm_0():
                    elm_size = ((available_height - total_gap) //
                                len(self.__content))
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.h = elm_size
                        elm.w = available_width
                        elm.x = self._pos[0] + self.__padding
                        elm.y = (self._pos[1] + self.__padding +
                                 ((self.__gap * (i + 1)) + (elm_size * i)))
                        if isinstance(elm, Container):
                            elm.__resize()
                else:
                    # Set all new size first
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.h = int(available_height * (size / 100))

                    if self.__gap == 0 and not self.__are_all_elm_0():
                        gap = self.__process_gap()
                    else:
                        gap = self.__gap

                    # Set all new pos then
                    for i, (elm, size) in enumerate(self.__content.items()):
                        elm.x = self._pos[0] + self.__padding
                        elm.w = available_width
                        elm.y = end_y + gap
                        end_y = ((elm.y if elm.y else 0) +
                                 (elm.h if elm.h else 0))
                        if isinstance(elm, Container):
                            elm.__resize()

    def __process_gap(self) -> int:
        if self._size and self._pos:
            if self.__way == 'VERTICAL':
                available_height = self._size[1] - 2 * self.__padding
                total_height = sum(elm.h if elm.h else 0
                                   for elm, _ in self.__content.items())
                return ((available_height - total_height) //
                        (len(self.__content) + 1))
            else:
                available_width = self._size[0] - 2 * self.__padding
                total_width = sum(elm.w if elm.w else 0
                                  for elm, _ in self.__content.items())
                return ((available_width - total_width) //
                        (len(self.__content) + 1))
        raise ValueError('size or pos not defined: cant process gap')

    def render(self) -> None:
        """Display contained elements ont screen"""
        if self._bg_color and self._pos and self._size:
            if self.padding_in_bg:
                rect_pos = self._pos
                rect_size = self._size
            else:
                print(f'Gap not in BG {self.__gap}')
                rect_pos = (
                    self._pos[0] + self.padding,
                    self._pos[1] + self.padding
                )
                rect_size = (
                    self._size[0] - 2 * self.padding,
                    self._size[1] - 2 * self.padding
                )

            temp_surface = pygame.Surface(rect_size, pygame.SRCALPHA)
            temp_surface.fill(self._bg_color)
            self._screen.screen.blit(temp_surface, rect_pos)
        for elm in self.__content:
            elm.render()

    @property
    def size(self) -> Optional[tuple[int, int]]:
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        if value:
            self._size = value
            # self.__resize()

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
            # self.__resize()

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
            # self.__resize()

    @property
    def gap(self) -> int:
        return self.__gap

    @gap.setter
    def gap(self, value: int) -> None:
        self.__gap = value
        self.__resize()

    @property
    def padding(self) -> int:
        return self.__padding

    @padding.setter
    def padding(self, value: int) -> None:
        self.__padding = value
        self.__resize()

    @property
    def padding_in_bg(self) -> bool:
        return self._gap_in_bg

    @padding_in_bg.setter
    def padding_in_bg(self, value: bool) -> None:
        self._gap_in_bg = value
