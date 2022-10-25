"""This module provides the RP To-Do CLI."""

from pathlib import Path
from typing import List, Optional

import typer

from kindtool import __app_name__, __version__, configinit, configcreate, templates

app = typer.Typer()
tpl = templates.Templates()

def is_valid(error: str) -> None:
    if error:
        typer.secho(
            f'{error}', fg=typer.colors.RED
        )
        raise typer.Exit(1)

@app.command(
    help="Creates a directory with configuration file."
)
def init(dest_dir: str) -> None:
    is_valid(tpl.prepare_dest_dir(dest_dir))
    init = configinit.ConfigInit(tpl)
    is_valid(init.create_content())
    return None

@app.command(
    help="Creates a new deployment based on an initalized directory."
)
def create(dest_dir: str) -> None:
    is_valid(tpl.has_valid_dest_dir(dest_dir))
    create = configcreate.ConfigCreate(tpl)
    is_valid(create.create_content())
    return None

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
