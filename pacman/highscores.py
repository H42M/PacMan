from dataclasses import dataclass
import json

MAX_HIGHSCORES = 10
MAX_PLAYER_NAME_LENGTH = 10


@dataclass(frozen=True, slots=True)
class HighscoreEntry:
    """Store one validated highscore entry."""

    name: str
    score: int


def validate_player_name(name: str) -> str:
    """Return a validated player name."""
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
    """Return a validated highscore value."""
    if score < 0:
        raise ValueError("Score is negative.")
    return score


def entry_from_raw(raw: object) -> HighscoreEntry | None:
    """Parse a highscore entry from raw JSON data."""
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
    """Convert a highscore entry to JSON data."""
    return {"name": entry.name, "score": entry.score}


def sort_highscores(entries: list[HighscoreEntry]) -> list[HighscoreEntry]:
    """Return highscores sorted from highest to lowest."""
    return (sorted(entries, key=lambda entry: entry.score,
                   reverse=True)[:MAX_HIGHSCORES])


def add_highscore(entries: list[HighscoreEntry],
                  name: str, score: int) -> list[HighscoreEntry]:
    """Add a highscore entry and return the sorted list."""
    name = validate_player_name(name)
    score = validate_score(score)
    entry = HighscoreEntry(name, score)
    entries.append(entry)
    return sort_highscores(entries)


def load_highscores(path: str) -> list[HighscoreEntry]:
    """Load highscores from a JSON file."""
    highscores_list: list[HighscoreEntry] = []
    try:
        with open(path, "r") as file:
            file_raw = json.load(file)
            if not isinstance(file_raw, list):
                raise ValueError("Highscore file must contain a list.")
            for line in file_raw:
                entry = entry_from_raw(line)
                if entry is not None:
                    highscores_list.append(entry)
        return sort_highscores(highscores_list)

    except (OSError, json.JSONDecodeError, ValueError):
        return []


def save_highscores(path: str, entries: list[HighscoreEntry]) -> bool:
    """Save highscores to a JSON file."""
    entries = sort_highscores(entries)
    raw_entries = []
    for entry in entries:
        raw_entries.append(entry_to_raw(entry))
    try:
        with open(path, "w") as file:
            json.dump(raw_entries, file, indent=4)
        return True
    except (OSError, TypeError):
        return False
