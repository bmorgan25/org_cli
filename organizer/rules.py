def get_folder_for_extension(
    extension: str, extension_map: dict, default_folder: str = "Misc"
) -> str:
    """
    Given a file extension, return the folder it should go into.
    Returns 'Misc' if the extension is not recognized.
    """
    return extension_map.get(extension.lower(), default_folder)
