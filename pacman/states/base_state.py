from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable, Optional, Protocol, cast

import pygame

from pacman.render.Screen import Screen


class StateError(Exception):
    """Raised when a screen state cannot be resolved."""


class KeyboardInput(Protocol):
    """Protocol for interactive elements that can receive keyboard input."""

    def handle_key(self, event: pygame.event.Event) -> None:
        """Handle a pygame keyboard event."""


class ScreenState(ABC):
    """Base class for UI/application screens."""

    def __init__(
        self,
        screen: Screen,
        state_manager: Optional[StateManager] = None
    ) -> None:
        """Initialize a screen state."""
        self._screen = screen
        self._state_manager = state_manager

    def bind_manager(self, state_manager: StateManager) -> None:
        """Attach this screen state to a state manager."""
        self._state_manager = state_manager

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        """Handle shared UI events.

        Returns False when the application should quit.
        """
        for event in events:
            if event.type == pygame.QUIT:
                return False

            mouse_pos = pygame.mouse.get_pos()

            for clickable in list(self._screen.clickables):
                if event.type == pygame.MOUSEMOTION:
                    clickable.update_hover(mouse_pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if clickable.is_clicked(mouse_pos):
                        clickable.execute()
                        break

                elif (
                    event.type == pygame.KEYDOWN
                    and hasattr(clickable, "handle_key")
                ):
                    cast(KeyboardInput, clickable).handle_key(event)

        return True

    @abstractmethod
    def update(self) -> None:
        """Update the screen state."""
        ...

    @abstractmethod
    def render(self) -> None:
        """Render the screen state."""
        ...


StatePayload = dict[str, object]
StateFactory = Callable[[Screen, "StateManager", StatePayload], ScreenState]


class StateManager:
    """Manage high-level UI/application screen states.

    This manager must not own gameplay rules. Gameplay remains owned by
    pacman.game_state.GameState.
    """

    MENU = 'MENU'
    SETTINGS = 'SETTINGS'
    HIGHSCORE = 'HIGHSCORE'
    PLAYING = 'PLAYING'
    GAMEOVER = 'GAMEOVER'
    VICTORY = 'VICTORY'
    INSTRUCTIONS = 'INSTRUCTIONS'

    def __init__(
        self,
        screen: Screen,
        initial_state: ScreenState | str,
        state_factories: Optional[dict[str, StateFactory]] = None,
    ) -> None:
        """Initialize the state manager."""
        self.__screen = screen
        self.__state_factories = {
            key.upper(): factory
            for key, factory in (state_factories or {}).items()
        }

        if isinstance(initial_state, str):
            self.__current_state = self.set_state(initial_state)
        else:
            initial_state.bind_manager(self)
            self.__current_state = initial_state

    def register_state(self, state: str, factory: StateFactory) -> None:
        """Register a screen state factory."""
        self.__state_factories[state.upper()] = factory

    def handle_events(self, events: list[pygame.event.Event]) -> bool:
        """Delegate event handling to the current screen state."""
        return self.__current_state.handle_events(events)

    def update(self) -> None:
        """Update the current screen state."""
        self.__current_state.update()

    def render(self) -> None:
        """Render the current screen state."""
        self.__current_state.render()

    def set_state(
        self,
        state: str,
        payload: StatePayload | None = None,
    ) -> ScreenState:
        """Switch to a registered screen state."""
        state_key = state.upper()
        factory = self.__state_factories.get(state_key)

        if factory is None:
            available = ', '.join(sorted(self.__state_factories))
            raise StateError(
                f"State '{state}' does not exist. "
                f"Available states: {available or 'none'}"
            )

        self.__screen.reset_clickables()
        new_state = factory(self.__screen, self, payload or {})
        self.__current_state = new_state
        return new_state

    @property
    def current_state(self) -> ScreenState:
        """Return the active screen state."""
        return self.__current_state
