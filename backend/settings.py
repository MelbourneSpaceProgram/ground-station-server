"""Maintains the settings.json file.

Reads this file when starting up the ground station and keeps it updated as
changes occur.
"""

import json
from typing import Any, Dict

from pathlib import Path


def get_root_dir() -> Path:
    """Return the root directory of the project."""
    return Path(__file__).absolute().parent


def get_data_dir() -> Path:
    """Return the path of the data volume."""
    return Path("/app/data")


def get_tle_dir() -> Path:
    """Return the directory containing TLEs."""
    tle_dir = get_data_dir() / "tle"
    if not tle_dir.exists():
        Path.mkdir(tle_dir)
    return tle_dir


DEFAULT_SETTINGS_FILE = get_root_dir() / "default.json"
SETTINGS_FILE = get_data_dir() / "settings.json"

USE_DEFAULTS = False

_cache: Dict[str, Any] = {}


def _load_settings() -> Dict[str, Any]:
    path = DEFAULT_SETTINGS_FILE
    if SETTINGS_FILE.exists() and not USE_DEFAULTS:
        path = SETTINGS_FILE
    with open(path, 'r') as file:
        return json.load(file)


def get(key: str) -> Any:
    """Retrieve the given setting."""
    global _cache
    if not _cache:
        _cache = _load_settings()
    return _cache[key]


def set(key: str, value: Any) -> None:
    """Set the given setting to the specified value.

    Only works for top-level keys.
    """
    global _cache
    if not _cache:
        _cache = _load_settings()
    _cache[key] = value

    # Write changes to file
    with open(SETTINGS_FILE, 'w') as file:
        json.dump(_cache, file, indent=2)
