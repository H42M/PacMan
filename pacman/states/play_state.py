from pygame.event import Event
# from pacman.game_config import GameConfig
from pacman.render.Screen import Screen
from pacman.render.RenderConfig import RenderConfig
from pacman.states.base_state import GameState, StateManager
from typing import Optional
from pacman.render.RenderMaze import RenderMaze
from pacman.render.Container import Container
import pygame


class PlayState(GameState):
    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None
                 ) -> None:
        super().__init__(screen, state_manager)

        # TODO: Define real maze size with GameConfig
        self.__maze = RenderMaze(screen, (300, 300))
        self.__game_ctn = self.__load_game_ctn()
        self.__menu_displayed = False

    def render(self) -> None:

        self._screen.clear()
        self.__game_ctn.render()
        if self.__menu_displayed:
            self._screen.menu.render()
        self._screen.flip()

    def handle_events(self, events: list[Event]) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__menu_displayed = not self.__menu_displayed
                    print(f'Display Menu {self.__menu_displayed}')
        return super().handle_events(events)

    def update(self) -> None:
        return super().update()

    def __load_game_ctn(self) -> Container:
        game_win_ctn = Container(self._screen, 'VERTICAL',
                                 (0, 0), padding=20,
                                 size=RenderConfig.screen_size)
        game_ctn = Container(self._screen, 'VERTICAL', bg_color=(0, 0, 0, 230))
        game_ctn.add_content({self.__maze: '90%'})

        game_win_ctn.add_content({game_ctn: '0%'})
        return game_win_ctn
