from collections import deque
from collections.abc import Callable

from pacman.maze_adapter import CellPosition
from pacman.ghost import GhostState
from pacman.player import PlayerState, Direction
from pacman.level import Level
from pacman.navigation import get_target_position


def find_next_step_toward(
        start: CellPosition,
        target: CellPosition,
        get_neighbors: Callable[[CellPosition], list[CellPosition]],
) -> CellPosition | None:
    if start == target:
        return None

    queue = deque([start])
    came_from: dict[CellPosition, CellPosition | None] = {start: None}

    while queue:
        current = queue.popleft()
        if current == target:
            break
        for neighbor in get_neighbors(current):
            if neighbor in came_from:
                continue
            came_from[neighbor] = current
            queue.append(neighbor)

    if target not in came_from:
        return None
    current = target
    while came_from[current] != start:
        previous = came_from[current]
        if previous is None:
            return None
        current = previous
    return current


def project_position_ahead(level: Level, start_position: CellPosition,
                           direction: Direction,
                           distance: int) -> CellPosition:
    current = start_position
    for _ in range(distance):
        next_position = get_target_position(level, current, direction)
        if next_position is None:
            return current
        current = next_position
    return current


def choose_normal_ghost_target(ghost: GhostState,
                               player: PlayerState,
                               level: Level) -> CellPosition:
    if ghost.name == "Blinky":
        return player.position
    if ghost.name == "Pinky":
        if player.current_direction is not None:
            return project_position_ahead(level, player.position,
                                          player.current_direction, 8)
        else:
            return player.position
    if ghost.name == "Inky":
        if player.current_direction is not None:
            return project_position_ahead(level, player.position,
                                          player.current_direction, 2)
        else:
            return player.position
    if ghost.name == "Clyde":
        dx = ghost.position[0] - player.position[0]
        dy = ghost.position[1] - player.position[1]
        distance = dx * dx + dy * dy
        if distance > 48:
            return player.position
        else:
            return ghost.spawn_position
    return player.position
