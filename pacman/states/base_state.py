from abc import ABC, abstractmethod
import pygame
from pacman.render.Screen import Screen
from typing import Union, Optional


class StateError(Exception):

    pass


class GameState(ABC):
    @abstractmethod
    def __init__(self, screen: Screen,
                 state_manager: Optional['StateManager'] = None
                 ) -> None:
        pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
        return True

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, screen: Screen) -> None:
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

    def render(self, screen: Screen) -> None:
        self.__current_state.render(screen)

    def set_state(self, state: str) -> GameState:
        from pacman.states.menu_state import MenuState
        from pacman.states.settingstate import SettingsState

        new_state: GameState
        self.__screen.reset_clickables()
        if state == self.MENU:
            new_state = MenuState(self.__screen, self)
        elif state.upper() == self.SETTINGS:
            new_state = SettingsState(self.__screen, self)
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
