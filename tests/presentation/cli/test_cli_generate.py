import pytest

from pathlib import Path

from typer.testing import CliRunner
from pytest_mock import mocker

from blueprint_forge import (
    create_cli,
    InvalidKnowledgeType
)


runner = CliRunner()

def test_cli_exposes_generate_command(cli_app):
    result = runner.invoke(cli_app, ["--help"])

    assert result.exit_code == 0
    assert "generate" in result.stdout

def test_generate_command_exposes_arguments_and_options(cli_app):
    result = runner.invoke(cli_app, ["generate", "--help"])

    assert result.exit_code == 0
    assert "source" in result.stdout
    assert "header" in result.stdout
    assert "footer" in result.stdout
    assert "output" in result.stdout

def test_generate_returns_error_when_command_is_invalid(cli_app):
    result = runner.invoke(
        cli_app,
        ["does-not-exist"],
    )

    assert result.exit_code != 0

def test_generate_accepts_valid_arguments_and_options(mocker):
    # Setup
    question_service = mocker.Mock()
    graphviz_service = mocker.Mock()

    cli_app = create_cli(
        graphviz_service=graphviz_service,
        question_service=question_service,
    )

    # Execution
    result = runner.invoke(
        cli_app,
        [
            "generate",
            "source.yaml",
            "--header", "header.dot",
            "--footer", "footer.dot",
            "--output", "graph.dot",
        ],
    )

    # Validation
    assert result.exit_code == 0
    graphviz_service.generate.assert_called_once_with(
        yaml_path=Path("source.yaml"),
        header_path=Path("header.dot"),
        footer_path=Path("footer.dot"),
        output_path=Path("graph.dot"),
    )

def test_generate_triggers_exception_block_on_exception(mocker):
    # Setup
    exception = InvalidKnowledgeType(
        expected="expected",
        received="bad_knowledge_type",
    )

    question_service = mocker.Mock()
    graphviz_service = mocker.Mock()

    graphviz_service.generate.side_effect = exception

    cli_app = create_cli(
        graphviz_service=graphviz_service,
        question_service=question_service,
    )

    # Execution
    result = runner.invoke(
        cli_app,
        [
            "generate",
            "source.yaml",
            "--header", "header.dot",
            "--footer", "footer.dot",
            "--output", "graph.dot",
        ],
    )

    # Validation
    assert result.exit_code == 1
    assert str(exception) in result.stderr