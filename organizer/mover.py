from pathlib import Path
import shutil

from organizer.rules import get_folder_for_extension


def organize_files(
    files: list[Path],
    destination: str,
    dry_run: bool = False,
    verbose: bool = False,
    extension_map: dict = None,
    default_folder: str = "Misc",
) -> dict:
    """
    Moves a list of files into subfolders within the destination directory,
    based on their file extensions.

    If dry_run is True, no files are actually moved.
    If verbose is True, prints a line for every file including skipped ones.

    Returns a summary dict with lists of moved and skipped files.
    """
    destination_path = Path(destination)

    summary = {
        "moved": [],
        "skipped": [],
    }

    for file in files:
        extension = file.suffix
        folder_name = get_folder_for_extension(
            extension, extension_map=extension_map, default_folder=default_folder
        )
        target_folder = destination_path / folder_name
        target_path = target_folder / file.name

        if target_path.exists():
            if verbose:
                print(f"  [SKIPPED] {file.name} already exists in {folder_name}/")
            summary["skipped"].append(file)
            continue

        if dry_run:
            print(f"  [DRY RUN] {file.name} -> {folder_name}/")
            summary["moved"].append(file)
            continue

        target_folder.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file), str(target_path))

        if verbose:
            print(f"  [MOVED] {file.name} -> {folder_name}/")

        summary["moved"].append(file)

    return summary
