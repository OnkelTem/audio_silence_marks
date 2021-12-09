import typer
from typing import Optional
from pathlib import Path
from .main import Target, main as app_main
from audio_silence_marks import __version__


def main():
    typer.run(cli)


def version_callback(value: bool):
    if value:
        typer.echo(f"{__version__}")
        raise typer.Exit()


def cli(
    path: Path = typer.Argument(
        ...,
        help='is a path to files. E.g: "."',
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=False,
        readable=True,
        resolve_path=False,
    ),
    glob: str = typer.Argument(
        ..., help="argument is a pattern for selecting files. E.g.: '**/*.mp3'"
    ),
    target: Target = typer.Option(
        Target.audipo, "--target", "-t", help="Target format for marks."
    ),
    noise: int = typer.Option(
        50,
        "--noise",
        "-n",
        help="Maximum volume of the noise treated as silence in -dB",
    ),
    duration: int = typer.Option(
        1000,
        "--duration",
        "-d",
        help="Minimum length of the silent interval in milliseconds",
    ),
    lst: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="Simply lists matched files. Useful for GLOB debugging.",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        help="Displays package version.",
        is_eager=True,
    ),
) -> None:
    """Processes audio files using FFmpeg filter silencedetect and outputs Audipo markers JSON with the list of
    spots placed in the middle of silence intervals.

    More info on using GLOBS: https://docs.python.org/3.8/library/glob.html
    """
    app_main(path, glob, target, noise, duration, lst)
