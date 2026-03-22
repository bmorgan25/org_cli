import click
import yaml
from orkanizer.config import load_config, DEFAULT_CONFIG_PATH


def save_config(config: dict) -> None:
    """
    Writes the config dict back to the config YAML file.
    """
    with open(DEFAULT_CONFIG_PATH, "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)


@click.command("config")
@click.option("--show", "-s", is_flag=True, help="Display the current config rules.")
@click.option(
    "--add-extension",
    "-a",
    nargs=2,
    metavar="EXT FOLDER",
    help="Add an extension to a folder (e.g. --add-extension .log Logs).",
)
@click.option(
    "--remove-extension",
    "-r",
    metavar="EXT",
    help="Remove an extension from the config.",
)
@click.option(
    "--add-folder", "-f", metavar="FOLDER", help="Add a new empty folder category."
)
def config_command(show, add_extension, remove_extension, add_folder):
    """
    View and modify the file organizer config rules.
    """
    try:
        config = load_config(DEFAULT_CONFIG_PATH)
    except (FileNotFoundError, ValueError) as e:
        click.echo(f"Config error: {e}")
        raise SystemExit(1)

    # --show
    if show:
        click.echo(f"\nConfig file: {DEFAULT_CONFIG_PATH}\n")
        click.echo(f"Default folder: {config['default_folder']}\n")
        click.echo("Rules:")
        for folder, extensions in config["folders"].items():
            exts = "  ".join(extensions)
            click.echo(f"  {folder:15} {exts}")
        click.echo()
        return

    # --add-folder
    if add_folder:
        if add_folder in config["folders"]:
            click.echo(f"Folder '{add_folder}' already exists.")
            raise SystemExit(1)
        config["folders"][add_folder] = []
        save_config(config)
        click.echo(f"Added folder '{add_folder}'.")
        return

    # --add-extension
    if add_extension:
        ext, folder = add_extension
        ext = ext.lower()

        if not ext.startswith("."):
            click.echo(f"Invalid extension '{ext}'. Extensions must start with a '.'")
            raise SystemExit(1)

        if folder not in config["folders"]:
            click.echo(
                f"Folder '{folder}' does not exist. Create it first with --add-folder {folder}"
            )
            raise SystemExit(1)

        # Check if the extension already exists in another folder
        for existing_folder, extensions in config["folders"].items():
            if ext in extensions:
                click.echo(
                    f"Extension '{ext}' is already assigned to '{existing_folder}'."
                )
                raise SystemExit(1)

        config["folders"][folder].append(ext)
        save_config(config)
        click.echo(f"Added '{ext}' to '{folder}'.")
        return

    # --remove-extension
    if remove_extension:
        ext = remove_extension.lower()
        for folder, extensions in config["folders"].items():
            if ext in extensions:
                extensions.remove(ext)
                save_config(config)
                click.echo(f"Removed '{ext}' from '{folder}'.")
                return
        click.echo(f"Extension '{ext}' not found in config.")
        raise SystemExit(1)

    # No option provided — show help
    click.echo(click.get_current_context().get_help())
