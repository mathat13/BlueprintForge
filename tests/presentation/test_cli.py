import pytest

from pathlib import Path
from unittest.mock import MagicMock, patch
from typer.testing import CliRunner

from blueprint_forge.presentation.cli import app

runner = CliRunner()

def test_cli_exposes_generate_command():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "generate" in result.stdout

def test_generate_exposes_source_argument():
    result = runner.invoke(app, ["generate", "--help"])

    assert result.exit_code == 0
    assert "source" in result.stdout

@pytest.mark.parametrize(
    "arguments",
    [
        pytest.param(["generate"], id="command_only"),
        pytest.param(["generate", "source.yaml"], id="command+source"),
        pytest.param(["generate", "source.yaml", "--header", "header.dot"], id="command+source+header"),
        pytest.param(["generate", "source.yaml", "--header", "header.dot", "--footer", "footer.dot"],
                     id="comand+source+header+footer"
                     ),
    ],
)
def test_generate_requires_all_arguments(arguments):
    result = runner.invoke(app, arguments)

    assert result.exit_code != 0

def test_generate_passes_arguments_to_application():
    mock_application = MagicMock()

    with patch(
        "blueprint_forge.presentation.cli.GraphvizService",
        return_value=mock_application,
    ):
        result = runner.invoke(
            app,
            [
                "generate",
                "source.yaml",
                "--header", "header.dot",
                "--footer", "footer.dot",
                "--output", "graph.dot",
            ],
        )

    assert result.exit_code == 0

    mock_application.generate.assert_called_once_with(
        yaml_path=Path("source.yaml"),
        header_path=Path("header.dot"),
        footer_path=Path("footer.dot"),
        output_path=Path("graph.dot"),
    )

def test_generate_returns_error_when_command_is_invalid():
    result = runner.invoke(
        app,
        ["does-not-exist"],
    )

    assert result.exit_code != 0