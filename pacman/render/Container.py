from pacman.render.RenderObj import RenderOBJ
from pacman.render.Screen import Screen

from typing import Optional, Union
import pygame


class Container(RenderOBJ):
    """Lay out render objects in a horizontal or vertical container."""

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
        display: bool = True
    ) -> None:
        """Initialize Container class."""
        super().__init__(screen, pos, size)
        self.__display = display
        self.__way = way
        self.__gap = gap
        self.__padding = padding
        self.__content: dict[RenderOBJ, int] = {}
        self._bg_color = bg_color
        self._gap_in_bg = True

    def __is_valid_percentage(self, value: str) -> bool:
        """Return whether a value is a valid percentage string."""
        if not isinstance(value, str) or not value.endswith('%'):
            return False
        try:
            new_value = int(value[:-1])
        except ValueError:
            return False
        if not (0 <= new_value <= 100):
            return False
        return True

    def __is_visible_child(self, elm: RenderOBJ) -> bool:
        """Return whether a child should be included in layout."""
        return not isinstance(elm, Container) or elm.display

    def __get_visible_content(self) -> dict[RenderOBJ, int]:
        """Return container content that is currently visible."""
        return {
            elm: size
            for elm, size in self.__content.items()
            if self.__is_visible_child(elm)
        }

    def __validate_visible_percentages(
        self,
        visible_content: dict[RenderOBJ, int]
    ) -> None:
        """Validate that visible content fits in the container."""
        if sum(size for _, size in visible_content.items()) > 100:
            raise ValueError("Sum of visible sizes is over 100% in container")

    def __are_all_elm_0(self, content: dict[RenderOBJ, int]) -> bool:
        """Return whether all content sizes are zero."""
        for _, size in content.items():
            if size != 0:
                return False
        return True

    def add_content(
        self,
        objs: Union[dict[RenderOBJ, str], list[dict[RenderOBJ, str]]]
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

        visible_content = self.__get_visible_content()
        self.__validate_visible_percentages(visible_content)
        self.resize()

    def resize(self) -> None:
        """Set size and pos for each contained elements."""
        if not self._size or not self._pos or not self.display:
            return

        visible_content = self.__get_visible_content()
        if not visible_content:
            return

        self.__validate_visible_percentages(visible_content)

        available_width = self._size[0] - 2 * self.__padding
        available_height = self._size[1] - 2 * self.__padding

        nb_gap = len(visible_content) + 1
        total_gap = nb_gap * self.__gap

        if self.__way == "HORIZONTAL":
            end_x = self._pos[0] + self.__padding + self.__gap

            if self.__are_all_elm_0(visible_content):
                elm_size = ((available_width - total_gap) //
                            len(visible_content))
                for elm, _ in visible_content.items():
                    elm.y = self._pos[1] + self.__padding
                    elm.w = elm_size
                    elm.x = end_x
                    elm.h = available_height
                    end_x = elm.x + elm_size + self.__gap
                    if isinstance(elm, Container):
                        elm.resize()
            else:
                for elm, size in visible_content.items():
                    elm.y = self._pos[1] + self.__padding
                    elm.w = int(available_width * (size / 100))

                if self.__gap == 0:
                    gap = self.__process_gap(visible_content)
                else:
                    gap = self.__gap

                for elm, _ in visible_content.items():
                    elm.x = end_x + gap
                    end_x = ((elm.x if elm.x else 0) +
                             (elm.w if elm.w else 0))
                    elm.h = available_height
                    if isinstance(elm, Container):
                        elm.resize()

        elif self.__way == 'VERTICAL':
            end_y = self._pos[1] + self.__padding

            if self.__are_all_elm_0(visible_content):
                elm_size = ((available_height - total_gap) //
                            len(visible_content))
                for i, (elm, _) in enumerate(visible_content.items()):
                    elm.h = elm_size
                    elm.w = available_width
                    elm.x = self._pos[0] + self.__padding
                    elm.y = (self._pos[1] + self.__padding +
                             ((self.__gap * (i + 1)) + (elm_size * i)))
                    if isinstance(elm, Container):
                        elm.resize()
            else:
                for elm, size in visible_content.items():
                    elm.h = int(available_height * (size / 100))

                if self.__gap == 0:
                    gap = self.__process_gap(visible_content)
                else:
                    gap = self.__gap

                for elm, _ in visible_content.items():
                    elm.x = self._pos[0] + self.__padding
                    elm.w = available_width
                    elm.y = end_y + gap
                    end_y = ((elm.y if elm.y else 0) +
                             (elm.h if elm.h else 0))
                    if isinstance(elm, Container):
                        elm.resize()
        else:
            raise ContainerError('Container way must be HORIZONTAL'
                                 f' or VERTICAL: {self.__way}')

    def __process_gap(self, content: dict[RenderOBJ, int]) -> int:
        """Compute the automatic gap between children."""
        if self._size and self._pos:
            if self.__way == 'VERTICAL':
                available_height = self._size[1] - 2 * self.__padding
                total_height = sum(elm.h if elm.h else 0
                                   for elm, _ in content.items())
                return ((available_height - total_height) //
                        (len(content) + 1))

            available_width = self._size[0] - 2 * self.__padding
            total_width = sum(elm.w if elm.w else 0
                              for elm, _ in content.items())
            return ((available_width - total_width) //
                    (len(content) + 1))

        raise ValueError('size or pos not defined: cant process gap')

    def render(self) -> None:
        """Display contained elements on screen."""
        if not self.display:
            return

        if self._bg_color and self._pos and self._size:
            if self.padding_in_bg:
                rect_pos = self._pos
                rect_size = self._size
            else:
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
        """Return the container size."""
        return self._size

    @size.setter
    def size(self, value: Optional[tuple[int, int]]) -> None:
        """Set the container size."""
        if value:
            self._size = value

    @property
    def w(self) -> Optional[int]:
        """Return the container width."""
        if self._size:
            return self._size[0]
        return None

    @w.setter
    def w(self, value: Optional[int]) -> None:
        """Set the container width."""
        if value:
            if self._size:
                self._size = (value, self._size[1])
            else:
                self._size = (value, 0)

    @property
    def h(self) -> Optional[int]:
        """Return the container height."""
        if self._size:
            return self._size[1]
        return None

    @h.setter
    def h(self, value: Optional[int]) -> None:
        """Set the container height."""
        if value:
            if self._size:
                self._size = (self._size[0], value)
            else:
                self._size = (0, value)

    @property
    def gap(self) -> int:
        """Return the container gap."""
        return self.__gap

    @gap.setter
    def gap(self, value: int) -> None:
        """Set the container gap."""
        self.__gap = value
        self.resize()

    @property
    def padding(self) -> int:
        """Return the container padding."""
        return self.__padding

    @padding.setter
    def padding(self, value: int) -> None:
        """Set the container padding."""
        self.__padding = value
        self.resize()

    @property
    def padding_in_bg(self) -> bool:
        """Return whether padding is included in the background."""
        return self._gap_in_bg

    @padding_in_bg.setter
    def padding_in_bg(self, value: bool) -> None:
        """Set whether padding is included in the background."""
        self._gap_in_bg = value

    @property
    def display(self) -> bool:
        """Return whether the container is visible."""
        return self.__display

    @display.setter
    def display(self, value: bool) -> None:
        """Set whether the container is visible."""
        self.__display = value
        self.resize()
        self._on_display_changed()

    def _on_display_changed(self) -> None:
        """Handle container visibility changes."""
        pass


class ContainerError(Exception):
    """Raised when container layout configuration is invalid."""

    pass
