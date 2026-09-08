import typer

from blueprint_forge.domain.exceptions.domain_exceptions import *
from blueprint_forge.application.exceptions.application_exceptions import *
from blueprint_forge.infrastructure.exceptions.infrastructure_exceptions import *

EXPECTED_EXCEPTIONS = (
        InvalidKnowledgeType,
        InvalidReasoningStatus,
        InvalidQuestionID,
        InvalidQuestionState,
        EmptyQuestionCollection,
        DuplicateQuestionID,
        InvalidPrerequisites,
        YAMLFileNotFound,
        ConfigFileNotFound,
    )
    
def handle_exception(exception: Exception) -> None:
    if isinstance(exception, EXPECTED_EXCEPTIONS):
        typer.echo(str(exception), err=True)
        raise typer.Exit(code=1)

    raise exception