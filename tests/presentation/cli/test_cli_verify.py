import pytest

from pathlib import Path
from typer.testing import CliRunner
from pytest_mock import mocker

from blueprint_forge import (
    create_cli,
    GraphvizService,
)

from blueprint_forge import InvalidKnowledgeType

runner = CliRunner()

def test_cli_exposes_verify_command(cli_app):
    result = runner.invoke(cli_app, ["--help"])

    assert result.exit_code == 0
    assert "verify" in result.stdout

def test_verify_command_exposes_arguments_and_options(cli_app):
    result = runner.invoke(cli_app, ["verify", "--help"])

    assert result.exit_code == 0
    assert "source" in result.stdout

def test_verify_accepts_valid_arguments_and_options(mocker):
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
            "verify",
            "source.yaml",
        ],
    )

    # Validation
    assert result.exit_code == 0
    question_service.load.assert_called_once_with(
        yaml_path=Path("source.yaml"),
    )

def test_verify_triggers_exception_block_on_exception(mocker):
    # Setup
    exception = InvalidKnowledgeType(
        expected="expected",
        received="bad_knowledge_type",
    )

    question_service = mocker.Mock()
    graphviz_service = mocker.Mock()

    question_service.load.side_effect = exception

    cli_app = create_cli(
        graphviz_service=graphviz_service,
        question_service=question_service,
    )

    # Execution
    result = runner.invoke(
        cli_app,
        [
            "verify",
            "source.yaml",
        ],
    )

    # Validation
    assert result.exit_code == 1
    assert str(exception) in result.stderr