from dataclasses import dataclass

MAX_HIGHSCORES = 10
MAX_PLAYER_NAME_LENGTH = 10


@dataclass(frozen=True, slots=True)
class HighscoreEntry:
    name: str
    score: int


def validate_player_name(name: str) -> str:
    if not name.strip():
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


def entry_to_raw(entry: HighscoreEntry) -> dict[str, object]:
    return {"name": entry.name, "score": entry.score}


def sort_highscores(entries: list[HighscoreEntry]) -> list[HighscoreEntry]:
    return (sorted(entries, key=lambda entry: entry.score,
                   reverse=True)[:MAX_HIGHSCORES])


def add_highscore(entries: list[HighscoreEntry],
                  name: str, score: int) -> list[HighscoreEntry]:
    name = validate_player_name(name)
    score = validate_score(score)
    entry = HighscoreEntry(name, score)
    entries.append(entry)
    return sort_highscores(entries)
