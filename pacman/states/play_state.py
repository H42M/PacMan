from typing import Optional

import pygame
from pygame.event import Event

from pacman.states.base_state import ScreenState, StateManager
from pacman.game_state import (
    GameState as GameplayState,
    GameOutcome,
    GameplayPhase,
)
from pacman.input import direction_from_key
from pacman.game_session import GameSession
from pacman.cheats import CheatState

from pacman.render.Container import Container
from pacman.render.RenderConfig import RenderConfig
from pacman.render.RenderGameplay import RenderGameplay
from pacman.render.Screen import Screen
from pacman.render.Window import Window


class PlayState(ScreenState):
    """UI screen for gameplay."""

    def __init__(
        self,
        screen: Screen,
        state_manager: Optional[StateManager] = None,
        game: Optional[GameplayState] = None,
        *,
        session: GameSession,
    ) -> None:
        """Initialize the gameplay screen state."""
        super().__init__(screen, state_manager)
        self.__game = game
        self.__session: GameSession = session
        self.__cheats = CheatState()
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
        self.__player_death_started_ms: Optional[int] = None
        self.__player_death_duration_ms = 1500
        if self.__render_gameplay:
            self.__render_gameplay.set_entities_move_delay(
                self.__player_move_delay_ms,
                self.__ghost_move_delay_ms)

    def handle_events(self, events: list[Event]) -> bool:
        """Handle gameplay input events."""
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.__skip_level()

                if event.key == pygame.K_F2:
                    self.__trigger_game_over()

                if event.key == pygame.K_F3:
                    self.__toggle_god_mode()

                if event.key == pygame.K_F4:
                    self.__toggle_ghost_freeze()

                if event.key == pygame.K_F5:
                    self.__add_life()

                if (event.key == pygame.K_ESCAPE and
                    (self.__game is None or
                     self.__game.phase is GameplayPhase.PLAYING)):
                    if self.__pause_menu.display:
                        self.__pause_menu.switch_display()
                    else:
                        self.__reset_pause_menu()
                        self.__pause_menu.switch_display()
                        self.__pause_menu.resize()

                elif (not self.__pause_menu.display and self.__game and
                        self.__game.outcome is GameOutcome.PLAYING and
                        self.__game.phase is GameplayPhase.PLAYING):
                    direction = direction_from_key(event.key)
                    if direction:
                        self.__game.queue_player_direction(direction)

        if self.__pause_menu.display:
            return super().handle_events(events)

        return True

    def update(self) -> None:
        """Update gameplay state and animations."""
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
            if self.__session.is_final_level:
                self._state_manager.set_state(
                    StateManager.VICTORY,
                    {"final_score": self.__game.score},
                )
            else:
                self.__start_next_level()
            return

        if self.__pause_menu.display:
            now = pygame.time.get_ticks()
            self.__last_timer_tick_ms = now
            self.__last_player_move_ms = now
            self.__last_ghost_move_ms = now
            return
        if self.__update_player_death_animation():
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
            self.__game.advance_player()
            self.__game.handle_player_ghost_collision(
                god_mode=self.__cheats.god_mode,)
            self.__last_player_move_ms = now

            if self.__game.phase is GameplayPhase.PLAYER_DYING:
                self.__start_player_death_animation(now)
                return
            if self.__game.outcome is not GameOutcome.PLAYING:
                return
            if self.__game.has_collected_all_pacgums():
                self.__game.outcome = GameOutcome.LEVEL_CLEARED
                return

        if ghost_elapsed >= self.__ghost_move_delay_ms:
            if not self.__cheats.ghost_freeze:
                self.__game.move_ghosts()
                self.__game.handle_player_ghost_collision(
                    god_mode=self.__cheats.god_mode,
                )
                if self.__game.phase is GameplayPhase.PLAYER_DYING:
                    self.__start_player_death_animation(now)
                    return
            self.__game.tick_ghost_timers(ghost_elapsed)
            self.__last_ghost_move_ms = now
            if self.__game.outcome is not GameOutcome.PLAYING:
                return

        # Animations:
        if self.__render_gameplay:
            from pacman.render.animation.AnimEntity import AnimSet
            if self.__game.frightened_timer_ms > 0:
                fright_timer = self.__game.frightened_timer_ms
                self.__render_gameplay.set_pacman_anim(AnimSet.BOOSTED)
                if fright_timer > 3000:
                    self.__render_gameplay.set_ghosts_anim(AnimSet.FRIGHTENED)
                else:
                    self.__render_gameplay.set_ghosts_anim(AnimSet.
                                                           FRIGHTENED_FLASHING)
            else:
                self.__render_gameplay.set_pacman_anim(AnimSet.NORMAL)
                self.__render_gameplay.set_ghosts_anim(AnimSet.NORMAL)

    def render(self) -> None:
        """Render the gameplay screen."""
        self._screen.clear()
        self.__renderer = self.__load_game()

        if self.__renderer:
            self.__renderer.render()
        else:
            self.__placeholder_ctn.render()

        self.__pause_menu.render()
        self._screen.flip()

    def __reset_pause_menu(self) -> None:
        """Rebuild the pause menu and clickable registry."""
        self._screen.reset_clickables()
        self.__pause_menu = self.__load_pause_menu()

    def __can_use_cheats(self) -> bool:
        """Return whether cheat actions can currently run."""
        return (self.__game is not None and
                self.__game.outcome is GameOutcome.PLAYING and
                self.__game.phase is GameplayPhase.PLAYING)

    def __skip_level(self) -> None:
        """Trigger a debug level clear."""
        if not self.__can_use_cheats() or self.__game is None:
            return
        self.__game.debug_trigger_level_clear()

    def __trigger_game_over(self) -> None:
        """Trigger a debug game over."""
        if not self.__can_use_cheats() or self.__game is None:
            return
        self.__game.debug_trigger_game_over()

    def __toggle_god_mode(self) -> None:
        """Toggle god mode if cheats are available."""
        if not self.__can_use_cheats():
            return
        self.__cheats.toggle_god_mode()

    def __toggle_ghost_freeze(self) -> None:
        """Toggle ghost freeze if cheats are available."""
        if not self.__can_use_cheats():
            return
        self.__cheats.toggle_ghost_freeze()

    def __add_life(self) -> None:
        """Add a life if cheats are available."""
        if not self.__can_use_cheats() or self.__game is None:
            return
        if self.__game.lives < 5:
            self.__game.lives += 1

    def __start_next_level(self) -> None:
        """Advance to the next configured level."""
        if self.__game is None:
            return
        self.__session.sync_from_game(self.__game)
        self.__session.advance_level()
        self.__game = self.__session.create_game_state()
        self.__render_gameplay = RenderGameplay(self._screen, self.__game)
        self.__render_gameplay.set_entities_move_delay(
            self.__player_move_delay_ms,
            self.__ghost_move_delay_ms,
        )
        self.__reset_pause_menu()
        now = pygame.time.get_ticks()
        self.__last_player_move_ms = now
        self.__last_ghost_move_ms = now
        self.__last_timer_tick_ms = now

    def __start_player_death_animation(self, now: int) -> None:
        """Prepare the player death animation."""
        from pacman.render.animation.AnimEntity import AnimSet
        self.__last_player_move_ms = now
        self.__last_ghost_move_ms = now
        self.__last_timer_tick_ms = now
        if self.__render_gameplay:
            self.__render_gameplay.set_pacman_anim(AnimSet.DEATH)

    def __update_player_death_animation(self) -> bool:
        """Update the player death animation state."""
        from pacman.render.animation.AnimEntity import AnimSet
        if (self.__game is None or self.__game.phase is
                not GameplayPhase.PLAYER_DYING):
            return False
        if not self.__render_gameplay:
            return False
        animator = self.__render_gameplay.pacman.animator
        if animator and animator.finished:
            self.__game.finish_player_death()
            self.__render_gameplay.set_pacman_anim(AnimSet.NORMAL)

        return True

    def __load_game(self) -> Container:
        """Build the gameplay HUD and renderer container."""
        from pacman.render.RenderText import RenderText
        from pacman.render.Image import RenderImg
        from pacman.utils.path import asset_path

        main_ctn = Container(self._screen, 'VERTICAL', pos=(0, 0),
                             size=RenderConfig.screen_size,
                             bg_color=RenderConfig.BLACK)
        if self.__render_gameplay and self.__game:
            lives_ctn_img = Container(self._screen, 'HORIZONTAL')
            for _ in range(self.__game.lives):
                lives_ctn_img.add_content(
                    {RenderImg(self._screen, asset_path('sprites/pacman.png'),
                               is_square=True): '20%'}
                )

            lives_ctn = Container(self._screen, 'HORIZONTAL', gap=30,
                                  padding=50)
            lives_ctn.add_content([
                    {RenderText(self._screen, 'Lives ',
                                font_family=RenderConfig.FONT,
                                font_size=18): '20%'},
                    {lives_ctn_img: '70%'}
                ])

            hud_ctn = Container(self._screen, 'HORIZONTAL')
            hud_ctn.add_content([

                {lives_ctn: '30%'},
                {RenderText(
                    self._screen,
                    f'Score: {self.__game.score}',
                    font_family=RenderConfig.FONT,
                    font_size=18): '20%'},
                {RenderText(
                    self._screen,
                    f'Time: {self.__game.remaining_time}',
                    font_family=RenderConfig.FONT,
                    font_size=18): '20%'},
                {RenderText(
                    self._screen,
                    f'Level: {self.__game.level.number}',
                    font_family=RenderConfig.FONT,
                    font_size=18): '20%'},
            ])

            main_ctn.add_content([
                {hud_ctn: '12%'},
                {self.__render_gameplay: '85%'}])

        return main_ctn

    def __load_placeholder(self) -> Container:
        """Build the fallback gameplay placeholder container."""
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
        """Build the pause menu window."""
        from pacman.render.Divider import Divider
        from pacman.render.RenderText import RenderText
        from pacman.render.interactives import Button

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

        title_ctn = Container(self._screen, 'VERTICAL', gap=40)
        title_ctn.add_content([
            {RenderText(self._screen, 'PAUSE', font_size=40): '0%'},
            {Divider(self._screen): '3%'}
        ])

        normal_area_ctn = Container(self._screen, 'VERTICAL')
        cheats_area_ctn = Container(
            self._screen,
            'VERTICAL',
            display=False,
            gap=10
        )

        def show_cheats_menu() -> None:
            """Switch the pause menu to cheat controls."""
            normal_area_ctn.display = False
            cheats_area_ctn.display = True
            disable_buttons(normal_buttons)
            enable_buttons(cheat_buttons)
            update_cheat_button_labels()
            window_menu.resize()

        def resume_game() -> None:
            """Close the pause menu."""
            window_menu.display = False

        def return_to_menu() -> None:
            """Return from gameplay to the main menu."""
            if self._state_manager:
                self._state_manager.set_state(StateManager.MENU)

        resume_button = Button(self._screen, 'Resume',
                               callback=resume_game,
                               color=RenderConfig.RED)
        cheats_menu_button = Button(
            self._screen,
            'Cheats Menu',
            callback=show_cheats_menu,
            color=RenderConfig.RED
        )
        return_to_menu_button = Button(
            self._screen,
            'Return to Menu',
            callback=return_to_menu,
            color=RenderConfig.RED
        )

        normal_buttons = [
            resume_button,
            cheats_menu_button,
            return_to_menu_button,
        ]
        normal_area_ctn.add_content([
            {resume_button: '30%'},
            {cheats_menu_button: '30%'},
            {return_to_menu_button: '30%'},
        ])

        def show_normal_menu() -> None:
            """Switch the pause menu to normal controls."""
            cheats_area_ctn.display = False
            normal_area_ctn.display = True
            disable_buttons(cheat_buttons)
            enable_buttons(normal_buttons)
            window_menu.resize()

        def toggle_god_mode_from_menu() -> None:
            """Toggle god mode from the pause menu."""
            self.__toggle_god_mode()
            update_cheat_button_labels()

        def toggle_ghost_freeze_from_menu() -> None:
            """Toggle ghost freeze from the pause menu."""
            self.__toggle_ghost_freeze()
            update_cheat_button_labels()

        god_mode_button = Button(
            self._screen,
            'God Mode: ON' if self.__cheats.god_mode else 'God Mode: OFF',
            callback=toggle_god_mode_from_menu,
            color=RenderConfig.RED
        )
        ghost_freeze_button = Button(
            self._screen,
            'Ghost Freeze: ON'
            if self.__cheats.ghost_freeze
            else 'Ghost Freeze: OFF',
            callback=toggle_ghost_freeze_from_menu,
            color=RenderConfig.RED
        )
        add_life_button = Button(
            self._screen,
            'Add Life',
            callback=self.__add_life,
            color=RenderConfig.RED
        )
        skip_level_button = Button(
            self._screen,
            'Skip Level',
            callback=self.__skip_level,
            color=RenderConfig.RED
        )
        back_button = Button(
            self._screen,
            'Back',
            callback=show_normal_menu,
            color=RenderConfig.RED
        )

        cheat_buttons = [
            god_mode_button,
            ghost_freeze_button,
            add_life_button,
            skip_level_button,
            back_button,
        ]

        def update_cheat_button_labels() -> None:
            """Refresh pause-menu cheat button labels."""
            god_mode_button.text = (
                'God Mode: ON' if self.__cheats.god_mode else 'God Mode: OFF'
            )
            ghost_freeze_button.text = (
                'Ghost Freeze: ON'
                if self.__cheats.ghost_freeze
                else 'Ghost Freeze: OFF'
            )

        def enable_buttons(buttons: list[Button]) -> None:
            """Register a list of buttons as clickable."""
            for button in buttons:
                self._screen.record_clickable(button)

        def disable_buttons(buttons: list[Button]) -> None:
            """Remove a list of buttons from click handling."""
            for button in buttons:
                self._screen.delete_clickable(button)

        cheats_area_ctn.add_content([
            {god_mode_button: '19%'},
            {ghost_freeze_button: '19%'},
            {add_life_button: '19%'},
            {skip_level_button: '19%'},
            {Divider(self._screen): '1%'},
            {back_button: '20%'},
        ])

        body_ctn = Container(self._screen, 'VERTICAL', padding=3, gap=10)
        body_ctn.add_content([
            {normal_area_ctn: '60%'},
            {cheats_area_ctn: '90%'},
        ])

        window_menu.add_content([
            {title_ctn: '10%'},
            {body_ctn: '65%'},
        ])

        disable_buttons(cheat_buttons)

        return window_menu
