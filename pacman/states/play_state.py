from typing import Optional

import pygame
from pygame.event import Event

from pacman.game_state import GameState as GameplayState, GameOutcome
from pacman.input import direction_from_key
from pacman.render.Container import Container
from pacman.render.RenderConfig import RenderConfig
from pacman.render.RenderGameplay import RenderGameplay
from pacman.render.Screen import Screen
from pacman.render.Window import Window
from pacman.states.base_state import ScreenState, StateManager


class PlayState(ScreenState):
    """UI screen for gameplay."""

    def __init__(
        self,
        screen: Screen,
        state_manager: Optional[StateManager] = None,
        game: Optional[GameplayState] = None,
        *,
        total_levels: int,
    ) -> None:
        super().__init__(screen, state_manager)
        self.__game = game
        self.__render_gameplay = (RenderGameplay(screen, game)
                                  if game else None)
        self.__renderer = self.__load_game()
        self.__placeholder_ctn = self.__load_placeholder()
        self.__pause_menu = self.__load_pause_menu()
        self.__last_player_move_ms = pygame.time.get_ticks()
        self.__player_move_delay_ms = 200
        self.__last_ghost_move_ms = pygame.time.get_ticks()
        self.__ghost_move_delay_ms = 500
        self.__last_timer_tick_ms = pygame.time.get_ticks()
        self.__countdown_timer_delay_ms = 1000
        self.__total_levels = total_levels
        if self.__render_gameplay:
            self.__render_gameplay.set_entities_move_delay(
                self.__player_move_delay_ms,
                self.__ghost_move_delay_ms)

    def handle_events(self, events: list[Event]) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_F1 and self.__game
                        and self.__game.outcome is GameOutcome.PLAYING):
                    self.__game.debug_trigger_level_clear()

                if (event.key == pygame.K_F2 and self.__game
                        and self.__game.outcome is GameOutcome.PLAYING):
                    self.__game.debug_trigger_game_over()

                if event.key == pygame.K_ESCAPE:
                    self.__pause_menu.switch_display()
                    if self.__pause_menu.display:
                        self.__pause_menu.resize()

                elif (not self.__pause_menu.display and self.__game and
                        self.__game.outcome is GameOutcome.PLAYING):
                    direction = direction_from_key(event.key)
                    if direction:
                        self.__game.queue_player_direction(direction)

        if self.__pause_menu.display:
            return super().handle_events(events)

        return True

    def update(self) -> None:
        if self.__game is None:
            return

        if (self.__game.outcome is GameOutcome.GAME_OVER
                and self._state_manager):
            self._state_manager.set_state(
                StateManager.GAMEOVER,
                {"final_score": self.__game.score},
            )
        if (self.__game.outcome is GameOutcome.LEVEL_CLEARED
                and self._state_manager):
            if self.__game.level.number >= self.__total_levels:
                self._state_manager.set_state(
                    StateManager.VICTORY,
                    {"final_score": self.__game.score},
                )
            return

        if self.__pause_menu.display:
            now = pygame.time.get_ticks()
            self.__last_timer_tick_ms = now
            self.__last_player_move_ms = now
            self.__last_ghost_move_ms = now
            return
        if self.__game.outcome is not GameOutcome.PLAYING:
            return

        now = pygame.time.get_ticks()
        level_timer_elapsed = now - self.__last_timer_tick_ms
        player_elapsed = now - self.__last_player_move_ms
        ghost_elapsed = now - self.__last_ghost_move_ms

        if level_timer_elapsed >= self.__countdown_timer_delay_ms:
            self.__game.timer_tick()
            self.__last_timer_tick_ms = now

        if player_elapsed >= self.__player_move_delay_ms:
            lives_before = self.__game.lives

            self.__game.advance_player()
            self.__game.handle_player_ghost_collision()
            self.__last_player_move_ms = now

            if self.__game.outcome is not GameOutcome.PLAYING:
                return
            if self.__game.lives < lives_before:
                self.__last_ghost_move_ms = now
                return
            if self.__game.has_collected_all_pacgums():
                print("Congratulations, you won!")
                self.__game.outcome = GameOutcome.LEVEL_CLEARED
                return

        if ghost_elapsed >= self.__ghost_move_delay_ms:
            self.__game.move_ghosts()
            self.__game.handle_player_ghost_collision()
            self.__game.tick_ghost_timers(ghost_elapsed)
            self.__last_ghost_move_ms = now
            if self.__game.outcome is not GameOutcome.PLAYING:
                return

    def render(self) -> None:
        self._screen.clear()
        self.__renderer = self.__load_game()
        if self.__renderer:
            self.__renderer.render()
        else:
            self.__placeholder_ctn.render()

        self.__pause_menu.render()
        self._screen.flip()

    def __load_game(self) -> Container:
        from pacman.render.RenderText import RenderText

        main_ctn = Container(self._screen, 'VERTICAL', pos=(0, 0),
                             size=RenderConfig.screen_size)
        if self.__render_gameplay and self.__game:
            hud_ctn = Container(self._screen, 'HORIZONTAL')
            hud_ctn.add_content([
                {RenderText(self._screen, f'Life: {self.__game.lives}'): '0%'},
                {RenderText(self._screen, f'Score: {self.__game.score}'
                            ): '0%'},
                {RenderText(self._screen, f'Time: {self.__game.remaining_time}'
                            ): '0%'},
                {RenderText(self._screen, f'Level: {self.__game.level.number}'
                            ): '0%'},
            ])

            main_ctn.add_content([
                {hud_ctn: '10%'},
                {self.__render_gameplay: '90%'}])

        return main_ctn

    def __load_placeholder(self) -> Container:
        from pacman.render.RenderText import RenderText

        container = Container(
            self._screen,
            'VERTICAL',
            size=RenderConfig.screen_size,
            pos=(0, 0),
            padding=120,
            bg_color=(0, 0, 0)
        )
        container.add_content({
            RenderText(
                self._screen,
                'PlayState preserved for future gameflow integration',
                font_size=30
            ): '0%'
        })
        return container

    def __load_pause_menu(self) -> Window:
        from pacman.render.Divider import Divider
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives import Button, SelectButton

        menu_size = 500
        menu_pos = (
            (RenderConfig.screen_size[0] - menu_size) // 2,
            (RenderConfig.screen_size[1] - menu_size) // 2
        )

        window_menu = Window(
            self._screen,
            'VERTICAL',
            menu_pos,
            (menu_size, menu_size),
            display_default=False,
            padding=20
        )

        title_ctn = Container(self._screen, 'VERTICAL')
        title_ctn.add_content([
            {RenderText(self._screen, 'PAUSE', font_size=40): '20%'},
            {Divider(self._screen): '1%'}
        ])

        normal_area_ctn = Container(self._screen, 'VERTICAL')
        cheats_area_ctn = Container(
            self._screen,
            'VERTICAL',
            display=False,
            gap=10
        )

        def show_cheats_menu() -> None:
            normal_area_ctn.display = False
            cheats_area_ctn.display = True
            window_menu.resize()

        def resume_game() -> None:
            window_menu.display = False

        def return_to_menu() -> None:
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        normal_area_ctn.add_content([
            {Button(self._screen, 'Resume', callback=resume_game): '30%'},
            {Button(self._screen, 'Cheats Menu',
                    callback=show_cheats_menu): '30%'},
            {Button(self._screen, 'Return to Menu',
                    callback=return_to_menu): '30%'},
        ])

        godmode_ctn = Container(self._screen, 'HORIZONTAL')
        godmode_ctn.add_content([
            {RenderText(self._screen, 'God mode'): '40%'},
            {SelectButton(self._screen, ['Disabled', 'Enabled']): '40%'},
        ])

        noclip_ctn = Container(self._screen, 'HORIZONTAL')
        noclip_ctn.add_content([
            {RenderText(self._screen, 'No Clip'): '40%'},
            {SelectButton(self._screen, ['Disabled', 'Enabled']): '40%'},
        ])

        frightened_ctn = Container(self._screen, 'HORIZONTAL')
        frightened_ctn.add_content([
            {RenderText(self._screen, 'Frightened Ghosts'): '40%'},
            {SelectButton(self._screen, ['Disabled', 'Enabled']): '40%'},
        ])

        def show_normal_menu() -> None:
            cheats_area_ctn.display = False
            normal_area_ctn.display = True
            window_menu.resize()

        cheats_area_ctn.add_content([
            {godmode_ctn: '0%'},
            {noclip_ctn: '0%'},
            {frightened_ctn: '0%'},
            {Button(self._screen, 'Back', callback=show_normal_menu): '0%'},
        ])

        body_ctn = Container(self._screen, 'VERTICAL', padding=3, gap=10)
        body_ctn.add_content([
            {normal_area_ctn: '60%'},
            {cheats_area_ctn: '60%'},
        ])

        window_menu.add_content([
            {title_ctn: '30%'},
            {body_ctn: '70%'},
        ])

        return window_menu
