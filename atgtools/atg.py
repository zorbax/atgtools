import platform
import sys
import time
from functools import wraps
from pathlib import Path
from typing import Dict, Any

import click

import atgtools.richard as r

# from . import __version__
# ic.configureOutput(prefix="-> ")

ROOT_COMMAND_HELP = """\b
ATGtools command-line interface
-------------------------------
"""


@click.group(
    invoke_without_command=False,
    no_args_is_help=True,
    help=ROOT_COMMAND_HELP,
)
@click.pass_context
def main(_: click.Context) -> None:
    """Creating Click group commands"""


def _echo_version() -> None:
    """
    Print the version of the software and plugins
    """
    # click.secho(f"atgcli version: {__version__}")
    click.echo(f"Python version: {platform.python_version()}")
    return None


def timeit(method: Any) -> Any:
    """
    Calculate the time it takes to run a method
    """

    @wraps(method)
    def wrapper(*args, **kargs):  # type: ignore
        starttime = time.time()
        result = method(*args, **kargs)
        endtime = time.time()
        print(end="\n")
        r.CONSOLE.print(f"Completed in: {(endtime - starttime)} minutes")

        return result

    return wrapper


@main.group(invoke_without_command=True)
@click.pass_context
def info(_: click .Context) -> None:
    """
    Display information about curret deployment.
    """
    click.secho("System versions", fg="green")
    _echo_version()
    # click.secho("\nInstalled plugins", fg="green")
    # _echo_plugins()

    click.secho("\nGetting help", fg="green")
    click.secho(
        "To get help with ATGtools, join us:\n" "https://discord.com/invite/ygGmxfphAR"
    )


@main.group()
@click.pass_context
def tools(_: click.Context) -> None:
    """Command lines tools for NGS preprocessing"""


@tools.command(
    "manifest",
    help="""\b
    Creates manifest file for Qiiime2 analysis

    FASTQ format filename: ID_R1.fastq.gz, ID_R2.fastq.gz
    """,
    no_args_is_help=True,
)
@click.option("--fastq-dir", "-d", metavar="\b", help="Folder with FASTQ files.")
@click.option(
    "--output-file",
    "-o",
    default="manifest.tsv",
    metavar="\b",
    show_default=True,
    help="TSV output format",
)
@click.option(
    "--csv-format",
    "-c",
    is_flag=True,
    required=False,
    default=False,
    help="CSV output format  [default: manifest.csv]",
)
def create_manifest(fastq_dir: str, output_file: str, csv_format: bool) -> None:
    """
    Create a manifest file (tsv/csv) from a directory containing FASTQ files.
    """
    _fastq_dir = Path(fastq_dir).resolve()
    if not any(Path(_fastq_dir).iterdir()):
        print(f"{_fastq_dir.stem}/ is empty")
        sys.exit(1)

    output_manifest: Dict[str, str] = {}
    output = Path.cwd() / output_file
    fq_files = [str(x.name) for x in _fastq_dir.glob("*fastq.gz")]
    prefix = sorted({"_".join(i.split("_")[:1]) for i in fq_files})

    def table_format(manifest: dict, file: Path, comma: bool = False) -> None:
        if comma:
            sep = ","
            out = Path(str(file).split(".", maxsplit=1)[0] + ".csv")
        else:
            sep = "\t"
            out = output

        for sample in prefix:
            manifest[sample] = (
                f"{_fastq_dir}/{sample}_R1.fastq.gz{sep}"
                f"{_fastq_dir}/{sample}_R2.fastq.gz"
            )

        if out.is_file():
            print("There is a previous manifest file")
            sys.exit()
        else:
            with open(out, "w", encoding="utf-8") as f:
                headers = [
                    "sample-id",
                    "forward-absolute-filepath",
                    "reverse-absolute-filepath",
                ]
                f.write(f"{sep}".join(headers) + "\n")

                for k, v in manifest.items():
                    f.write(f"{k}{sep}{v}" + "\n")

    table_format(output_manifest, output, csv_format)


if __name__ == "__main__":
    main()
