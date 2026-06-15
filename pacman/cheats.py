from dataclasses import dataclass


@dataclass
class CheatState:
    god_mode: bool = False
    ghost_freeze: bool = False
    speed_boost: bool = False

    def toggle_god_mode(self) -> None:
        self.god_mode = not self.god_mode

    def toggle_ghost_freeze(self) -> None:
        self.ghost_freeze = not self.ghost_freeze

    def toggle_speed_boost(self) -> None:
        self.speed_boost = not self.speed_boost
