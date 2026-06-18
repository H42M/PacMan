from dataclasses import dataclass


@dataclass
class CheatState:
    """Store enabled cheat flags for gameplay."""

    god_mode: bool = False
    ghost_freeze: bool = False
    speed_boost: bool = False

    def toggle_god_mode(self) -> None:
        """Toggle god mode on or off."""
        self.god_mode = not self.god_mode

    def toggle_ghost_freeze(self) -> None:
        """Toggle ghost movement freeze on or off."""
        self.ghost_freeze = not self.ghost_freeze

    def toggle_speed_boost(self) -> None:
        """Toggle speed boost on or off."""
        self.speed_boost = not self.speed_boost
