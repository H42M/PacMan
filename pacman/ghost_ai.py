from __future__ import annotations

from collections import deque
from collections.abc import Callable

from pacman.ghost import GhostState
from pacman.level import Level
from pacman.maze_adapter import CellPosition
from pacman.navigation import get_target_position, get_valid_neighbor_positions
from pacman.player import Direction, PlayerState


BLINKY = "Blinky"
PINKY = "Pinky"
INKY = "Inky"
CLYDE = "Clyde"

PINKY_LOOKAHEAD = 10
INKY_LOOKAHEAD = 5
CLYDE_FLEE_DISTANCE_SQUARED = 64


def find_next_step_toward(
        start: CellPosition,
        target: CellPosition,
        get_neighbors: Callable[[CellPosition], list[CellPosition]],
) -> CellPosition | None:
    """Return the first step on a shortest path to a target."""
    if start == target:
        return None

    queue: deque[CellPosition] = deque([start])
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
    while True:
        previous = came_from[current]
        if previous is None:
            return None
        if previous == start:
            return current
        current = previous


def choose_normal_ghost_step(
        ghost: GhostState,
        ghosts: list[GhostState],
        player: PlayerState,
        level: Level,
) -> CellPosition | None:
    """Choose the next normal-mode step for a ghost."""
    if ghost.name == CLYDE and is_clyde_too_close(ghost, player):
        return choose_flee_step(level, ghost.position, player.position)

    target = choose_normal_ghost_target(ghost, ghosts, player, level)

    next_step = find_next_step_toward(
        ghost.position,
        target,
        lambda position: get_valid_neighbor_positions(level, position),
    )
    if next_step is not None:
        return next_step

    if target != player.position:
        return find_next_step_toward(
            ghost.position,
            player.position,
            lambda position: get_valid_neighbor_positions(level, position),
        )

    return None


def choose_normal_ghost_target(
        ghost: GhostState,
        ghosts: list[GhostState],
        player: PlayerState,
        level: Level,
) -> CellPosition:
    """Choose the target cell for a normal-mode ghost."""
    if ghost.name == BLINKY:
        return player.position

    if ghost.name == PINKY:
        return get_ambush_target(level, player, PINKY_LOOKAHEAD)

    if ghost.name == INKY:
        return get_inky_target(level, ghosts, player)

    if ghost.name == CLYDE:
        return player.position

    return player.position


def get_ambush_target(
        level: Level,
        player: PlayerState,
        distance: int,
) -> CellPosition:
    """Return a target ahead of the player's current direction."""
    if player.current_direction is None:
        return player.position

    return project_position_ahead(
        level,
        player.position,
        player.current_direction,
        distance,
    )


def get_inky_target(
        level: Level,
        ghosts: list[GhostState],
        player: PlayerState,
) -> CellPosition:
    """Return Inky's mirrored ambush target."""
    ahead = get_ambush_target(level, player, INKY_LOOKAHEAD)
    blinky = find_ghost_by_name(ghosts, BLINKY)

    if blinky is None:
        return ahead

    target = mirror_position(blinky.position, ahead)
    if is_playable_position(level, target):
        return target

    return ahead


def is_clyde_too_close(
        ghost: GhostState,
        player: PlayerState,
) -> bool:
    """Return whether Clyde should flee from the player."""
    return (
        squared_distance(ghost.position, player.position)
        <= CLYDE_FLEE_DISTANCE_SQUARED
    )


def choose_flee_step(
        level: Level,
        position: CellPosition,
        threat: CellPosition,
) -> CellPosition | None:
    """Choose a neighboring cell farthest from a threat."""
    neighbors = get_valid_neighbor_positions(level, position)
    if not neighbors:
        return None

    return max(
        neighbors,
        key=lambda neighbor: squared_distance(neighbor, threat),
    )


def project_position_ahead(
        level: Level,
        start_position: CellPosition,
        direction: Direction,
        distance: int,
) -> CellPosition:
    """Project a position forward through legal cells."""
    current = start_position

    for _ in range(distance):
        next_position = get_target_position(level, current, direction)
        if next_position is None:
            return current
        current = next_position

    return current


def find_ghost_by_name(
        ghosts: list[GhostState],
        name: str,
) -> GhostState | None:
    """Return the ghost with a matching name."""
    for ghost in ghosts:
        if ghost.name == name:
            return ghost
    return None


def mirror_position(
        origin: CellPosition,
        point: CellPosition,
) -> CellPosition:
    """Return a point mirrored across another position."""
    origin_x, origin_y = origin
    point_x, point_y = point

    return (
        point_x + (point_x - origin_x),
        point_y + (point_y - origin_y),
    )


def is_playable_position(level: Level, position: CellPosition) -> bool:
    """Return whether a position is inside and not solid."""
    return (
        level.is_inside(position)
        and position not in level.maze.solid_positions
    )


def squared_distance(first: CellPosition, second: CellPosition) -> int:
    """Return the squared distance between two cells."""
    first_x, first_y = first
    second_x, second_y = second
    dx = first_x - second_x
    dy = first_y - second_y
    return dx * dx + dy * dy
