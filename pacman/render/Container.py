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
                                          tuple[int, int, int, int]]] = None,
                 display: bool = True
                 ) -> None:
        """Initialize Container class"""
        super().__init__(screen, pos, size)
        self.__display = display
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
            if isinstance(elm, Container) and not elm.display:
                continue
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
        # if sum(size for obj, size in self.__content.items()) > 100:
            total_size = 0
            for obj, size in self.__content.items():
                if not isinstance(obj, Container) or obj.display:
                    total_size += size
            if total_size > 100:
                raise ValueError("Sum of sizes is over 100% in container")
        self.resize()

    def resize(self) -> None:
        if self._size and self._pos and self.display:
            # ← construire une vue filtrée une seule fois
            visible = {elm: size for elm, size in self.__content.items()
                       if not isinstance(elm, Container) or elm.display}
            if not visible:
                return

            available_width = self._size[0] - 2 * self.__padding
            available_height = self._size[1] - 2 * self.__padding
            nb_gap = len(visible) + 1
            total_gap = nb_gap * self.__gap

            if self.__way == "HORIZONTAL":
                end_x = self._pos[0] + self.__padding + self.__gap
                if self.__are_all_elm_0():
                    elm_size = (available_width - total_gap) // len(visible)
                    for elm, size in visible.items():
                        elm.y = self._pos[1] + self.__padding
                        elm.w = elm_size
                        elm.x = end_x
                        elm.h = available_height
                        end_x = elm.x + elm_size + self.__gap
                        if isinstance(elm, Container):
                            elm.resize()
                else:
                    for elm, size in visible.items():
                        elm.y = self._pos[1] + self.__padding
                        elm.w = int(available_width * (size / 100))

                    gap = (self.__gap if self.__gap != 0 else
                           self.__process_gap(visible))
                    for elm, size in visible.items():
                        elm.x = end_x + gap
                        end_x = (elm.x or 0) + (elm.w or 0)
                        elm.h = available_height
                        if isinstance(elm, Container):
                            elm.resize()

            elif self.__way == 'VERTICAL':
                end_y = self._pos[1] + self.__padding
                if self.__are_all_elm_0():
                    elm_size = (available_height - total_gap) // len(visible)
                    for i, (elm, size) in enumerate(visible.items()):
                        elm.h = elm_size
                        elm.w = available_width
                        elm.x = self._pos[0] + self.__padding
                        elm.y = (self._pos[1] + self.__padding +
                                 (self.__gap * (i + 1)) + (elm_size * i))
                        if isinstance(elm, Container):
                            elm.resize()
                else:
                    for elm, size in visible.items():
                        elm.h = int(available_height * (size / 100))

                    gap = (self.__gap if self.__gap != 0 else
                           self.__process_gap(visible))
                    for elm, size in visible.items():
                        elm.x = self._pos[0] + self.__padding
                        elm.w = available_width
                        elm.y = end_y + gap
                        end_y = (elm.y or 0) + (elm.h or 0)
                        if isinstance(elm, Container):
                            elm.resize()
            else:
                raise ContainerError(f'Container way must be HORIZONTAL'
                                     f' or VERTICAL: {self.__way}')

    def __process_gap(self, visible: dict) -> int:
        if self._size and self._pos:
            if self.__way == 'VERTICAL':
                available_height = self._size[1] - 2 * self.__padding
                total_height = sum(elm.h or 0 for elm in visible)
                return (available_height - total_height) // (len(visible) + 1)
            else:
                available_width = self._size[0] - 2 * self.__padding
                total_width = sum(elm.w or 0 for elm in visible)
                return (available_width - total_width) // (len(visible) + 1)
        raise ValueError('size or pos not defined: cant process gap')

    def render(self) -> None:
        """Display contained elements ont screen"""
        if self._bg_color and self._pos and self._size and self.display:
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
        if self.__display:
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
        self.resize()

    @property
    def padding(self) -> int:
        return self.__padding

    @padding.setter
    def padding(self, value: int) -> None:
        self.__padding = value
        self.resize()

    @property
    def padding_in_bg(self) -> bool:
        return self._gap_in_bg

    @padding_in_bg.setter
    def padding_in_bg(self, value: bool) -> None:
        self._gap_in_bg = value

    @property
    def display(self) -> bool:
        return self.__display

    @display.setter
    def display(self, value: bool) -> None:
        self.__display = value


class ContainerError(Exception):

    pass
