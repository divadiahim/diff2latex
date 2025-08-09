# pyright: basic
# fuck strict typing ong
from typing import TextIO
import click
from .core import Diff2Latex
from .core.utils import CharColorizer
import os
from string import Template
import shutil
import tempfile
import subprocess
from . import __file__ as package_root

TEMPLATE_PATH = os.path.join(os.path.dirname(package_root), "templates/template.tex")


def _load_template() -> Template:
    """Load the LaTeX template from the package."""
    with open(TEMPLATE_PATH, "r") as template_file:
        return Template(template_file.read())


@click.group()
@click.version_option()
@click.option("--font-family", default="Fira Code", help="Font family for the LaTeX document")
@click.option("--font-size", default="10pt", help="Font size for the LaTeX document")
@click.option("--highlight", default="none", help="Colorizer style for syntax highlighting")
@click.option("--pdf-output", is_flag=True, help="Generate PDF output instead of LaTeX")
@click.pass_context
def cli(ctx, **kwargs) -> None:
    """diff2latex - Output diffs in latex"""
    ctx.ensure_object(dict)
    ctx.obj.update(kwargs)


@cli.command()
@click.pass_context
@click.argument("diff_file_path", type=click.File("r"))
@click.argument("output_dir", type=click.Path(file_okay=False, dir_okay=True, writable=True))
def build(ctx, diff_file_path: TextIO, output_dir: str) -> None:
    """Build LaTeX from a diff file."""
    os.makedirs(output_dir, exist_ok=True)

    colorizer = CharColorizer(style_name=ctx.obj["highlight"] if ctx.obj["highlight"] != "none" else None) #?
    differ = Diff2Latex.build(diff_file_path, colorizer=colorizer)
    lines = differ.to_latex()

    base_name = "diff_output"
    tex_path = os.path.join(output_dir, f"{base_name}.tex")
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")

    template = _load_template().substitute(
        font=ctx.obj["font_family"],
        fontsize=ctx.obj["font_size"],
        content=lines,
    )
    with open(tex_path, "w") as tex_file:
        tex_file.write(template)

    if ctx.obj.get("pdf_output", False):
        if shutil.which("lualatex") is None:
            raise RuntimeError("lualatex not found in PATH. Please install it.")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_tex = os.path.join(tmpdir, "temp.tex")
            with open(tmp_tex, "w") as f:
                f.write(template)

            subprocess.run(["lualatex", "-interaction=nonstopmode", tmp_tex], cwd=tmpdir, check=True)
            subprocess.run(["lualatex", "-interaction=nonstopmode", tmp_tex], cwd=tmpdir, check=True)

            tmp_pdf = os.path.join(tmpdir, "temp.pdf")
            shutil.move(tmp_pdf, pdf_path)

    click.echo(f"LaTeX written to: {tex_path}")
    if ctx.obj.get("pdf_output", False):
        click.echo(f"PDF written to: {pdf_path}")
    

def main():
    """Main entry point for the CLI."""
    cli()
