from pathlib import Path
import yaml

DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config.yml"


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> dict:
    """
    Loads and validates the given config yaml.
    Returns the config as a dict.
    """
    if not config_path.exists():
        raise FileNotFoundError()

    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    return validate_config(raw_config)


def validate_config(raw_config: dict) -> dict:
    """
    Validate the given configuration dictionary.
    Raise a ValueError if config missing values or malformed
    """
    if not isinstance(raw_config, dict):
        raise ValueError("Config file must be a YAML mapping at the top level")

    if "folders" not in raw_config:
        raise ValueError("Config file is missing the required key: 'folders'")

    if not isinstance(raw_config["folders"], dict):
        raise ValueError(
            "'folders' must be a mapping of folder names to file extensions"
        )

    for folder, extensions in raw_config["folders"].items():
        if not isinstance(extensions, list):
            raise ValueError(f"File extensions for '{folder}' must be a list!")
        for ext in extensions:
            if not isinstance(ext, str) or not ext.startswith("."):
                raise ValueError(
                    f"All extensions must be a string and start with '.' - Invalid extension: {ext}"
                )

    if "default_folder" in raw_config:
        raw_config["default_folder"] = "Misc"

    return raw_config


def build_extension_map(config: dict) -> dict:
    """
    Inverts the folder -> ext mapping from config files.
    Ex: {"Images": [".jpg", ".png"]} -> {".jpg": "Images", ".png": Images}
    """

    extensions_map = {}

    for folder, extensions in config.items():
        for ext in extensions:
            extensions_map[ext.lower()] = folder

    return extensions_map
