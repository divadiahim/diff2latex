import click
from .core import Diff2Latex
import os
from . import __file__ as package_root

TEMPLATE_PATH = os.path.join(os.path.dirname(package_root), "templates/template.tex")


def _load_template() -> str:
    """Load the LaTeX template from the package."""
    with open(TEMPLATE_PATH, "r") as template_file:
        return template_file.read()
    
def _replace_placeholder(template: str, placeholder: str, value: str) -> str:
    """Replace a placeholder in the template with a given value."""
    result = template.replace(placeholder, value)
    return result


@click.group()
@click.version_option()
@click.option(
    "--output-file", type=click.File("w"), help="Path to the output LaTeX file"
)
@click.option(
    "--font-family", default="Courier", help="Font family for the LaTeX document"
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
    lines = differ.parse_diff_lines()
    for line in lines:
        print(line.to_latex())
    
    template = _load_template()
    template = _replace_placeholder(template, "%font%", ctx.obj["font_family"])
    template = _replace_placeholder(template, "%fontsize%", ctx.obj["font_size"])
    output_file.write(template)
    

    pass


def main():
    """Main entry point for the CLI."""
    cli()
