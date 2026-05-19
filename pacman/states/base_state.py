from abc import ABC, abstractmethod
import pygame
from pacman.render.Screen import Screen
from typing import Union, Optional


class StateError(Exception):

    pass


class GameState(ABC):
    def __init__(self, screen: Screen,
                 state_manager: Optional['StateManager'] = None
                 ) -> None:
        self._screen = screen
        self._state_manager = state_manager

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEMOTION:
                for clickable in self._screen.clickables:
                    clickable.update_hover(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONDOWN:
                for clickable in self._screen.clickables:
                    if clickable.is_hovered:
                        clickable.execute()
        return True

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass


class StateManager:
    MENU = 'MENU'
    SETTINGS = 'SETTINGS'
    PLAYING = 'PLAYING'

    def __init__(self, screen: Screen,
                 initial_state: Union[GameState, str],
                 ) -> None:
        self.__screen = screen
        if isinstance(initial_state, str):
            self.__current_state = self.set_state(initial_state)
        else:
            self.__current_state = initial_state

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        return self.__current_state.handle_events(events)

    def update(self) -> None:
        self.__current_state.update()

    def render(self) -> None:
        self.__current_state.render()

    def set_state(self, state: str) -> GameState:
        from pacman.states.menu_state import MenuState
        from pacman.states.settingstate import SettingsState
        from pacman.states.play_state import PlayState

        new_state: GameState
        self.__screen.reset_clickables()
        if state.upper() == self.MENU:
            new_state = MenuState(self.__screen, self)
        elif state.upper() == self.SETTINGS:
            new_state = SettingsState(self.__screen, self)
        elif state.upper() == self.PLAYING:
            new_state = PlayState(self.__screen, self)
        else:
            raise StateError(f'State {state} doesnt exist {self.MENU}')

        self.current_state = new_state
        return new_state

    @property
    def current_state(self) -> GameState:
        return self.__current_state

    @current_state.setter
    def current_state(self, value: GameState) -> None:
        self.__current_state = value
