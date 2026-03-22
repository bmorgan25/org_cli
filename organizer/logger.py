import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path.home() / ".organizer_history.json"


def _load_history() -> list:
    """
    Return the history of file moves.
    """
    if not HISTORY_FILE.exists():
        return []

    else:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)


def log_moves(moves) -> None:
    """
    Adds the list of moves to the history file
    """
    history = _load_history()

    new_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "moves": moves,
    }

    history.append(new_entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def get_last_run() -> dict | None:
    """
    Returns the most recent run entry, or None if history is empty.
    """
    history = _load_history()
    return history[-1] if history else None
