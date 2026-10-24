import json
import logging
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

DATA_DIR = Path(__file__).resolve().parent / "data"
LEGACY_FILE = DATA_DIR / "habits.json"
logger = logging.getLogger(__name__)


def _file_for_user(user_id: int | None = None) -> Path:
    if user_id is None:
        return LEGACY_FILE
    if isinstance(user_id, bool) or not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("user_id must be a positive integer")
    return DATA_DIR / "users" / f"{user_id}.json"


def load_habits(user_id: int | None = None) -> list[dict]:
    path = _file_for_user(user_id)
    try:
        with path.open("r", encoding="utf-8") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, OSError) as error:
        logger.warning("Could not read habits from %s: %s", path, error)
        return []

    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        logger.warning("Habit data in %s has an unexpected format", path)
        return []
    return data


def save_habits(user_id: int | None, habits: list[dict]) -> None:
    if not isinstance(habits, list) or any(not isinstance(item, dict) for item in habits):
        raise ValueError("habits must be a list of objects")

    path = _file_for_user(user_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_name = None
    try:
        with NamedTemporaryFile(
            "w", encoding="utf-8", dir=path.parent, delete=False
        ) as data_file:
            json.dump(habits, data_file, indent=2, ensure_ascii=False)
            data_file.write("\n")
            temporary_name = data_file.name
        os.replace(temporary_name, path)
    finally:
        if temporary_name and os.path.exists(temporary_name):
            os.unlink(temporary_name)
