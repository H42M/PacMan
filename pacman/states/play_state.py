from pygame.event import Event
# from pacman.game_config import GameConfig
from pacman.render.Screen import Screen
from pacman.render.RenderConfig import RenderConfig
from pacman.states.base_state import GameState, StateManager
from typing import Optional
from pacman.game.GameWorld import GameWorld
from pacman.render.RenderWorld import RenderWorld
from pacman.render.Container import Container
from pacman.render.Window import Window
import pygame


class PlayState(GameState):
    def __init__(self, screen: Screen,
                 state_manager: Optional[StateManager] = None
                 ) -> None:
        super().__init__(screen, state_manager)

        # TODO: Define real maze size with GameConfig
        self.__world = GameWorld()
        self.__render_world = RenderWorld(self._screen, self.__world)
        self.__game_ctn = self.__load_game_ctn()
        self.__menu_ctn = self.__load_menu()

    def render(self) -> None:
        self._screen.clear()
        self.__game_ctn.render()
        self.__menu_ctn.render()
        self._screen.flip()

    def handle_events(self, events: list[Event]) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                from pacman.entities.Player import Player
                if event.key == pygame.K_ESCAPE:
                    self.__menu_ctn.switch_display()

                if event.key == pygame.K_w:
                    self.__world.player.dir = Player.UP
                if event.key == pygame.K_s:
                    self.__world.player.dir = Player.DOWN
                if event.key == pygame.K_a:
                    self.__world.player.dir = Player.LEFT
                if event.key == pygame.K_d:
                    self.__world.player.dir = Player.RIGHT
        return super().handle_events(events)

    def update(self) -> None:
        from pacman.entities.Player import Player
        if not self.__menu_ctn.display:
            player = self.__world.player
            maze = self.__world.maze

            player.tick()

            if player.dir != Player.NONE and not player.is_moving:
                moves = {
                    Player.UP:    (0, -1, 'n'),
                    Player.RIGHT: (1,  0, 'e'),
                    Player.DOWN:  (0,  1, 's'),
                    Player.LEFT:  (-1, 0, 'w'),
                }
                dx, dy, wall = moves[player.dir]
                nx, ny = player.pos[0] + dx, player.pos[1] + dy

                player.dir_str = wall
                if 0 <= nx < maze.w and 0 <= ny < maze.h:
                    if not maze.get_cell_wall(player.pos, wall):
                        player.start_moving((nx, ny))

    def __load_game_ctn(self) -> Container:
        game_win_ctn = Container(self._screen, 'VERTICAL',
                                 (0, 0), padding=20,
                                 size=RenderConfig.screen_size)
        game_ctn = Container(self._screen, 'VERTICAL', bg_color=(0, 0, 0, 230))
        game_ctn.add_content({self.__render_world: '90%'})

        game_win_ctn.add_content({game_ctn: '0%'})
        return game_win_ctn

    def __load_menu(self) -> Window:
        # TODO: Menu shouldnt be defined here
        """Generate an exemple of menu if needed"""
        from pacman.render.Container import Container
        from pacman.render.Window import Window
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives.Button import Button
        from pacman.render.Divider import Divider
        from pacman.render.interactives.Input import Input

        # WINDOW MENU
        menu_size = 500
        menu_pos = ((RenderConfig.screen_size[0] - menu_size) // 2,
                    (RenderConfig.screen_size[1] - menu_size) // 2)
        window_menu = Window(self._screen, 'VERTICAL', menu_pos,
                             (menu_size, menu_size), display_default=True,
                             padding=20)
        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([{
            RenderText(self._screen, "Menu", font_size=40): '20%'},
            {Divider(self._screen): "1%"}])

        # INPUT CONTAINER
        input_ctn = Container(self._screen, 'HORIZONTAL', )
        input_ctn.add_content([
            {RenderText(self._screen, 'Player name'): '40%'},
            {Input(self._screen, placeholder="Ex: player_1"): '60%'},
            ])

        def on_quit() -> None:
            if self._state_manager:
                self._state_manager.set_state('MENU')

        save_quit_ctn = Container(self._screen, 'HORIZONTAL', gap=20)
        save_quit_ctn.add_content([
            {Button(self._screen, 'Save changes'): '0%'},
            {Button(self._screen, 'Quit', callback=on_quit): '0%'},
        ])

        sett_area_ctn = Container(self._screen, 'VERTICAL')
        sett_area_ctn.add_content([
            {input_ctn: '30%'},
            {Button(self._screen, 'Restart'): '30%'}
            ])

        # BTNS CONTAINER
        btn_ctn = Container(self._screen, 'VERTICAL', padding=3, gap=10)
        btn_ctn.add_content([
            {sett_area_ctn: '60%'},
            {Divider(self._screen): '1%'},
            {save_quit_ctn: '30%'}
            ])

        window_menu.add_content([
            {title_ctn: '30%'},
            {btn_ctn: '70%'},
            ])

        return window_menu
