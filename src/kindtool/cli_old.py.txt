"""This module provides the RP To-Do CLI."""

from pathlib import Path
from typing import Optional
import os

import typer

from kindtool import __app_name__, __version__, cmdinit, cmdup, cmddestroy, templates

app = typer.Typer()

def is_valid(error: str) -> None:
    if error:
        typer.secho(
            f'{error}', fg=typer.colors.RED
        )
        raise typer.Exit(1)

# what's wrong with this?
# https://typer.tiangolo.com/tutorial/commands/context/
def get_dest_dir(ctx: typer.Context) -> str:
    dest_dir=os.getcwd()
    if ctx.args:
        dest_dir=ctx.args[0]
    return dest_dir

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Creates a directory with configuration file."
)
def init(ctx: typer.Context) -> None:
    dest_dir=get_dest_dir(ctx)
    tpl = templates.Templates(dest_dir=dest_dir)
    init = cmdinit.CmdInit(tpl)
    is_valid(init.create_content())
    return None

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Creates a new deployment based on an initalized directory."
)
def up(ctx: typer.Context) -> None:
    dest_dir=get_dest_dir(ctx)
    tpl = templates.Templates(dest_dir=dest_dir)
    up = cmdup.CmdUp(tpl)
    is_valid(up.run())
    return None

@app.command(
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="Deletes a running clustery."
)
def destroy(ctx: typer.Context) -> None:
    dest_dir=os.getcwd()
    index = 0
    if ctx.args:
        if ctx.args[0].lower() != "-f":
            dest_dir=ctx.args[0]
            index+=1

    force=False
    if len(ctx.args) >index:
        if ctx.args[index].lower() == "-f":
            force = True

    tpl = templates.Templates(dest_dir=dest_dir)
    destroy = cmddestroy.CmdDestroy(tpl)
    is_valid(destroy.run(force))
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
