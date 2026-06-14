from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .builder import DocxBuilder

app = typer.Typer(help="doc-maker — Convert custom Markdown to Word documents.")


@app.command()
def convert(
    input_file: Path = typer.Argument(..., metavar="INPUT", help="Path to .md file"),
    output:     Optional[Path] = typer.Option(None, "--output", "-o", help="Output .docx path"),
    template:   Optional[Path] = typer.Option(None, "--template", "-t", help="Template .docx path"),
):
    if not input_file.exists():
        typer.echo(f"Error: {input_file} not found", err=True)
        raise typer.Exit(1)

    out     = output or input_file.with_suffix(".docx")
    md_text = input_file.read_text(encoding="utf-8")

    builder = DocxBuilder(template_path=template)
    doc     = builder.build(md_text)
    doc.save(str(out))
    typer.echo(f"Saved: {out}")


def main():
    app()


if __name__ == "__main__":
    main()
