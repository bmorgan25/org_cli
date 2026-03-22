from pathlib import Path


def scan_directory(directory: str) -> list[Path]:
    """
    Scans the given directory and returns a list of file Paths.
    Only returns files (not subdirectories) at the top level.
    Skips hidden files like .DS_Store.
    """
    target = Path(directory)

    if not target.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not target.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    files = [
        item
        for item in target.iterdir()
        if item.is_file() and not item.name.startswith(".")
    ]

    return files
