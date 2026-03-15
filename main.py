from organizer.scanner import scan_directory
from organizer.mover import organize_files
import click


@click.command()
@click.argument("directory")
@click.option("--dry-run", is_flag=True, help="Preview changes without moving any files.")
@click.option("--verbose", is_flag=True, help="Print detailed output for every file.")
def main(directory, dry_run, verbose):
    """
    Organize the files in a given directory into subfolders based on their file extensions.
    """
    
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

    summary = organize_files(files, directory, dry_run=dry_run, verbose=verbose)

    click.echo(f"\nDone! {len(summary['moved'])} moved, {len(summary['skipped'])} skipped.")


if __name__ == "__main__":
    main()