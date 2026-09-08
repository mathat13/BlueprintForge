import pytest
from typing import List

from tests.factories.DataFactories import QuestionYamlFactory

from blueprint_forge import (
    Question,
    create_cli,
    GraphvizService,
    QuestionService,
)

@pytest.fixture
def cli_app():
    return create_cli(
        graphviz_service=GraphvizService(
            question_service=QuestionService(),
        ),
        question_service=QuestionService(),
    )

@pytest.fixture
def questions() -> List[Question]:
    data = QuestionYamlFactory.create_batch(5)

    return [
        Question.from_dict(
            id=question_id,
            data=question_data,
        )
        for question_data in data
        for question_id, question_data in question_data.items()
    ]

@pytest.fixture
def question() -> "Question":
    data = QuestionYamlFactory()
    question_id, question_data = next(iter(data.items()))

    return Question.from_dict(
            id=question_id,
            data=question_data,
        )

@pytest.fixture
def make_question(question_yaml) -> Question:
    question_id, question_data = next(iter(question_yaml.items()))
    
    return Question.from_dict(
        id=question_id,
        data=question_data
        )