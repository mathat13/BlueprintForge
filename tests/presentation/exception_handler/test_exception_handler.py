import pytest
import typer

from pathlib import Path

from blueprint_forge import (
    handle_exception,
)

from blueprint_forge.domain.exceptions.domain_exceptions import *
from blueprint_forge.application.exceptions.application_exceptions import *
from blueprint_forge.infrastructure.exceptions.infrastructure_exceptions import *

@pytest.mark.parametrize(
    "exception",
    [
        # domain
        pytest.param(
            InvalidKnowledgeType(
                    expected="expected",
                    received="bad_knowledge_type"
                                    ),
            id="invalid-knowledge-type",
        ),
        pytest.param(
            InvalidReasoningStatus(
                 expected="expected",
                 received="bad_reasoning_status"
                                   ),
            id="invalid-reasoning-status",
        ),
        pytest.param(
            InvalidQuestionID(received="bad_id"),
            id="invalid-question-id",
        ),
        pytest.param(
            InvalidQuestionState(
                 reason="invalid_state",
                 received="invalid_question",
                 ),
            id="invalid-question-state",
        ),
        pytest.param(
            EmptyQuestionCollection(),
            id="empty-question-collection",
        ),
        pytest.param(
            DuplicateQuestionID(question_id="bad_question_id"),
            id="duplicate-question-id",
        ),
        # application
        pytest.param(
            InvalidPrerequisites(reason="bad_prerequisites"),
            id="invalid-prerequisites",
        ),
        # infrastructure
        pytest.param(
            YAMLFileNotFound(path=Path("/fake_path.mkv")),
            id="source-file-not-found",
        ),
        pytest.param(
            ConfigFileNotFound(path=Path("/fake_path.mkv")),
            id="config-file-not-found",
        ),
    ],
)

def test_exception_handler_handles_expected_exceptions(exception, capsys):
    # Execution
    with pytest.raises(typer.Exit) as exc_info:
        handle_exception(exception=exception)

    # Validation
    assert exc_info.value.exit_code == 1

    captured = capsys.readouterr()
    assert str(exception) in captured.err

def test_exception_handler_propagates_unexpected_exception():
    # Setup
    exception = FileNotFoundError()

    # Execution / Validation
    with pytest.raises(FileNotFoundError) as exc_info:
        handle_exception(exception=exception)

    assert exc_info.value is exception