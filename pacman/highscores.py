from dataclasses import dataclass

MAX_HIGHSCORES = 10
MAX_PLAYER_NAME_LENGTH = 10


@dataclass(frozen=True, slots=True)
class HighscoreEntry:
    name: str
    score: int


def validate_player_name(name: str) -> str:
    if not name:
        raise ValueError("Enter a valid name.")
    name = name.strip()
    if len(name) > MAX_PLAYER_NAME_LENGTH:
        raise ValueError("Name can not be more than "
                         f"{MAX_PLAYER_NAME_LENGTH} characters")
    if not all(char.isalnum() or char == " " for char in name):
        raise ValueError("Enter a valid name.")
    return name


def validate_score(score: int) -> int:
    if score < 0:
        raise ValueError("Score is negative.")
    return score


def entry_from_raw(raw: object) -> HighscoreEntry | None:
    if not isinstance(raw, dict):
        return None
    name = raw.get("name")
    score = raw.get("score")

    if not isinstance(name, str) or not isinstance(score, int):
        return None

    try:
        return HighscoreEntry(validate_player_name(name),
                              validate_score(score))
    except ValueError:
        return None
