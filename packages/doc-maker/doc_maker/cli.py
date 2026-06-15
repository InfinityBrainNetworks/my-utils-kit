from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from .builder import DocxBuilder
from .templates import REGISTRY, DEFAULT_STYLE

app = typer.Typer(help="doc-maker — Convert custom Markdown to Word documents.")


@app.command()
def convert(
    input_file: Path = typer.Argument(..., metavar="INPUT", help="Path to .md file"),
    output:     Optional[Path] = typer.Option(None,          "--output", "-o", help="Output .docx path"),
    style:      str            = typer.Option(DEFAULT_STYLE, "--style",  "-s", help=f"Template style. Available: {', '.join(REGISTRY)}"),
    base_doc:   Optional[Path] = typer.Option(None,          "--base-doc",     help="Optional .docx file to inherit Word styles from"),
):
    if not input_file.exists():
        typer.echo(f"Error: {input_file} not found", err=True)
        raise typer.Exit(1)

    if style not in REGISTRY:
        typer.echo(f"Error: unknown style '{style}'. Available: {', '.join(REGISTRY)}", err=True)
        raise typer.Exit(1)

    out     = output or input_file.with_suffix(".docx")
    md_text = input_file.read_text(encoding="utf-8")

    builder = DocxBuilder(style=style, base_doc=base_doc)
    doc     = builder.build(md_text)
    doc.save(str(out))
    typer.echo(f"Saved: {out}  [style: {style}]")


def main():
    app()


if __name__ == "__main__":
    main()
