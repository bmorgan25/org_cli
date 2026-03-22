from orkanizer.config import DEFAULT_CONFIG_PATH, load_config, build_extension_map
from orkanizer.logger import log_moves
from orkanizer.scanner import scan_directory
from orkanizer.mover import organize_files, undo_last_run
from orkanizer.config_commands import config_command
import click


@click.group()
def cli():
    """
    A parent command to delegate to subcommands
    """
    pass


@cli.command()
@click.argument("directory")
@click.option(
    "--dry-run", "-d", is_flag=True, help="Preview changes without moving any files."
)
@click.option(
    "--verbose", "-v", is_flag=True, help="Print detailed output for every file."
)
@click.option("--undo", "-u", is_flag=True, help="Reverse the last organization run")
def organize(directory, dry_run, verbose, undo):
    """
    Organize the files in a given directory into subfolders based on their file extensions.
    """

    if undo:
        undo_last_run()
        return

    try:
        config = load_config(DEFAULT_CONFIG_PATH)
        extension_map = build_extension_map(config)
        default_folder = config["default_folder"]
    except (FileNotFoundError, ValueError) as e:
        click.echo(f"Config error: {e}")
        raise SystemExit(1)

    click.echo(f"Scanning directory {directory}...\n")

    try:
        files = scan_directory(directory)
    except (FileNotFoundError, NotADirectoryError) as e:
        click.echo(f"Error: {e}")
        raise SystemExit(1)

    if not files:
        click.echo("No files found. Exiting.")
        return

    click.echo(f"Found {len(files)} file(s).\n")

    if dry_run:
        click.echo("--- DRY RUN --- (no files will be moved)\n")

    summary = organize_files(
        files,
        directory,
        dry_run=dry_run,
        verbose=verbose,
        extension_map=extension_map,
        default_folder=default_folder,
    )

    if not dry_run and summary["move_records"]:
        log_moves(summary["move_records"])

    click.echo(
        f"\nDone! {len(summary['moved'])} moved, {len(summary['skipped'])} skipped."
    )


cli.add_command(config_command)

if __name__ == "__main__":
    cli()
