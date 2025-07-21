import click
from .core import Diff2Latex
import os
from string import Template
from . import __file__ as package_root

TEMPLATE_PATH = os.path.join(os.path.dirname(package_root), "templates/template.tex")


def _load_template() -> Template:
    """Load the LaTeX template from the package."""
    with open(TEMPLATE_PATH, "r") as template_file:
        return Template(template_file.read())


@click.group()
@click.version_option()
@click.option(
    "--output-file", type=click.File("w"), help="Path to the output LaTeX file"
)
@click.option(
    "--font-family", default="Fira Code", help="Font family for the LaTeX document"
)
@click.option("--font-size", default="10pt", help="Font size for the LaTeX document")
@click.pass_context
def cli(ctx, **kwargs) -> None:
    """diff2latex - Output diffs in latex"""
    ctx.ensure_object(dict)
    ctx.obj.update(kwargs)


@cli.command()
@click.pass_context
@click.argument("diff_file_path", type=click.File("r"))
@click.argument("output_file", type=click.File("w"))
def convert(ctx, diff_file_path: click.File, output_file: click.File) -> None:
    diff_lines = diff_file_path.readlines()
    differ = Diff2Latex(srclines=diff_lines)
    lines = differ.parse_diff_lines().to_latex()

    template = _load_template().substitute(
        font=ctx.obj["font_family"],
        fontsize=ctx.obj["font_size"],
        content=lines,
    )
    output_file.write(template)


def main():
    """Main entry point for the CLI."""
    cli()
