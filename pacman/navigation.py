from pacman.level import Level
from pacman.maze_adapter import CellPosition, Wall
from pacman.player import Direction


def get_target_position(
        level: Level,
        position: CellPosition,
        direction: Direction,
) -> CellPosition | None:
    if direction == Direction.UP:
        movement = (0, -1)
        blocking_wall = Wall.NORTH
    elif direction == Direction.DOWN:
        movement = (0, 1)
        blocking_wall = Wall.SOUTH
    elif direction == Direction.LEFT:
        movement = (-1, 0)
        blocking_wall = Wall.WEST
    elif direction == Direction.RIGHT:
        movement = (1, 0)
        blocking_wall = Wall.EAST
    else:
        raise ValueError("Direction is incorrect.")

    x, y = position
    dx, dy = movement
    target = (x + dx, y + dy)

    if target in level.maze.solid_positions:
        return None
    blocked = level.walls_at(position) & blocking_wall
    if level.is_inside(target) and not blocked:
        return target
    else:
        return None


def get_valid_neighbor_positions(level: Level,
                                 position: CellPosition) -> list[CellPosition]:
    neighbors = []
    for direction in Direction:
        target = get_target_position(level, position, direction)
        if target is not None:
            neighbors.append(target)
    return neighbors


def get_direction_between(start: CellPosition,
                          target: CellPosition) -> Direction | None:
    start_x, start_y = start
    target_x, target_y = target
    dx = target_x - start_x
    dy = target_y - start_y

    if (dx, dy) == (0, -1):
        return Direction.UP
    if (dx, dy) == (0, 1):
        return Direction.DOWN
    if (dx, dy) == (-1, 0):
        return Direction.LEFT
    if (dx, dy) == (1, 0):
        return Direction.RIGHT
    return None
