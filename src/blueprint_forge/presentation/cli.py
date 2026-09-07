from pathlib import Path

import typer

from blueprint_forge.application.graphviz_service import GraphvizService

app = typer.Typer()


@app.callback()
def cli():
    """Translate knowledge-base YAML into Graphviz representations."""
    pass

@app.command()
def generate(
    source: Path = typer.Argument(...),
    header: Path = typer.Option(..., "--header"),
    footer: Path = typer.Option(..., "--footer"),
    output: Path = typer.Option(..., "--output"),
):
    application = GraphvizService()
    
    application.generate(
        yaml_path=source,
        header_path=header,
        footer_path=footer,
        output_path=output,
    )


def main() -> None:
    app()
    
if __name__ == "__main__":
    app()