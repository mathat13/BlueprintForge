from pathlib import Path

import typer

from blueprint_forge.application.graphviz_service import GraphvizService
from blueprint_forge.application.question_service import QuestionService
from blueprint_forge.presentation.exception_handler import handle_exception

def create_cli(
    graphviz_service: GraphvizService,
    question_service: QuestionService,
) -> typer.Typer:

    app = typer.Typer()

    @app.callback()
    def cli():
        """Translate knowledge-base YAML into Graphviz representations."""
        pass

    @app.command()
    def verify(
        source: Path = typer.Argument(...)
        ):
        try:
            question_service.load(yaml_path=source)
            typer.echo("Source is valid!")
        except Exception as exc:
            typer.echo("Source is invalid! Please see reason below:", err=True)
            handle_exception(exc)

    @app.command()
    def generate(
        source: Path = typer.Argument(...),
        header: Path = typer.Option(..., "--header"),
        footer: Path = typer.Option(..., "--footer"),
        output: Path = typer.Option(..., "--output"),
        ):
        try:
            typer.echo(f"Attempting graphviz generation from {source}!")
            graphviz_service.generate(
                yaml_path=source,
                header_path=header,
                footer_path=footer,
                output_path=output,
            )
            typer.echo(f"Generation complete! Please find output at {output}")

        except Exception as exc:
            typer.echo("Generation failed. Please see reason below:", err=True)
            handle_exception(exc)

    return app