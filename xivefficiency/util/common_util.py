import importlib
from types import ModuleType


def make_unique(items: list[str]) -> str:
    """Makes sure that all column names are unique.
    If they are not, a number is appended to the end of the name.
    Empty names are ignored."""
    unique_entries = []
    for entry in items:
        if (entry == ""):
            continue
        if entry in unique_entries:
            i = 1
            while f"{entry}_{i}" in unique_entries:
                i += 1
            entry = f"{entry}_{i}"
        unique_entries.append(entry)
    return unique_entries


def import_if_exists(module: str, package: str) -> bool | ModuleType:
    try:
        return importlib.import_module(f".{module}", package=package)
    except ModuleNotFoundError:
        return False
