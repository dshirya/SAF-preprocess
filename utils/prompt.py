import click
from typing import Dict, List
import utils.folder as folder

def get_user_input_folder_processing(dir_names: List[str], file_type: str) -> Dict[int, str]:
    click.echo(f"\nFolders with {file_type} files:")
    for i, dir_name in enumerate(dir_names, start=1):
        file_paths = folder.get_file_paths(dir_name)
        click.echo(f"{i}. {dir_name}, {len(file_paths)} files")

    click.echo("\nWould you like to process each folder above sequentially?")
    is_sequentially_processed = click.confirm("(Default: Y)", default=True)

    if is_sequentially_processed:
        return {idx: name for idx, name in enumerate(dir_names, start=1)}

    selected = click.prompt("Enter comma-separated folder indices (e.g., 1,3,5)", type=str)
    indices = [int(i.strip()) for i in selected.split(",") if i.strip().isdigit() and int(i.strip()) in range(1, len(dir_names)+1)]
    return {i: dir_names[i - 1] for i in indices}

def prompt_folder_progress(i: int, dir_name: str, dirs_total_count: int) -> None:
    count = 70
    click.echo("\n")
    click.echo("=" * count)
    click.echo(f"Processing {dir_name}, ({i} out of {dirs_total_count})")
    click.echo("=" * count)
