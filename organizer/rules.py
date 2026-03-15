EXTENSION_MAP = {
    # Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".webp": "Images",
    ".svg": "Images",
    ".heic": "Images",

    # Videos
    ".mp4": "Videos",
    ".mov": "Videos",
    ".avi": "Videos",
    ".mkv": "Videos",

    # Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",

    # Documents
    ".pdf": "Documents",
    ".docx": "Documents",
    ".doc": "Documents",
    ".txt": "Documents",
    ".md": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".pptx": "Documents",

    # Code
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".html": "Code",
    ".css": "Code",
    ".json": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".sh": "Code",

    # Archives
    ".zip": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
}


def get_folder_for_extension(extension: str) -> str:
    """
    Given a file extension, return the folder it should go into.
    Returns 'Misc' if the extension is not recognized.
    """
    return EXTENSION_MAP.get(extension.lower(), "Misc")