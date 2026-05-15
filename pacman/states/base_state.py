from abc import ABC, abstractmethod
import pygame


class GameState(ABC):
    @abstractmethod
    def handle_events(self, event) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def render(self, screen) -> None:
        pass


class StateManager:
    MENU = 'MENU'
    SETTINGS = 'SETTINGS'
    PLAYING = 'PLAYING'

    def __init__(self, initial_state: GameState) -> None:
        self.__current_state = initial_state

    def handle_events(self, event: list[pygame.event.Event]) -> None:
        self.__current_state.handle_events(event)

    def update(self) -> None:
        self.__current_state.update()

    def render(self, screen) -> None:
        self.__current_state.render(screen)

    @property
    def current_state(self):
        return self.__current_state

    @current_state.setter
    def current_state(self, value):
        self.__current_state = value
