import pytest
from pydantic import (
    ValidationError,
)

from blueprint_forge import QuestionData

from tests.factories.DataFactories import (
    QuestionDataFactory,
    ReasoningDataFactory,
    KnowledgeDataFactory,
    QuestionDataWithoutKnowledgeFactory,
    QuestionDataWithoutReasoningFactory,
    QuestionDataWithoutWorksheetPathFactory,
    QuestionDataWithoutKnowledgePathFactory,
    QuestionDataWithoutKnowledgeTypeFactory,
    QuestionDataWithoutReasoningStatusFactory,
    QuestionDataWithoutQuestionFactory,
    QuestionDataWithoutSummaryFactory,
)

@pytest.mark.parametrize(
    "data",
    [
        # question
        pytest.param(QuestionDataFactory(question="string"), id="string_question"),
        # summary
        pytest.param(QuestionDataFactory(summary="string"), id="string_summary"),
        # reasoning.status
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(status="string")), id="string_reasoning_status"),
        # reasoning.worksheet_path
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(worksheet_path="string")), id="string_reasoning_worksheet_path"),
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(worksheet_path=None)), id="null_worksheet_path"),
        pytest.param(QuestionDataWithoutWorksheetPathFactory(), id="no_worksheet_path"),
        # knowledge
        pytest.param(QuestionDataFactory(knowledge=None), id="null_knowledge"),
        pytest.param(QuestionDataWithoutKnowledgeFactory(), id="no_knowledge"),
        # knowledge.type
        pytest.param(QuestionDataFactory(knowledge=KnowledgeDataFactory(type="string")), id="string_knowledge_type"),
        # knowledge.path
        pytest.param(QuestionDataFactory(knowledge=KnowledgeDataFactory(path="string")), id="string_knowledge_path"),
        # prerequisites
        pytest.param(QuestionDataFactory(prerequisites=["node_1", "node_2"]), id="list_of_string_prerequisites"),
        pytest.param(QuestionDataFactory(prerequisites=[]), id="empty_list_prerequisites"),
    ],
)

def test_QuestionData_validates_on_valid_data(data):
    QuestionData.model_validate(data)

@pytest.mark.parametrize(
    "data",
    [
        # question
        pytest.param(QuestionDataFactory(question=123), id="incorrect_question_type"),
        pytest.param(QuestionDataFactory(question=None), id="null_question"),
        pytest.param(QuestionDataWithoutQuestionFactory(), id="no_question"),
        # summary
        pytest.param(QuestionDataFactory(summary=123), id="incorrect_summary_type"),
        pytest.param(QuestionDataFactory(summary=None), id="null_summary"),
        pytest.param(QuestionDataWithoutSummaryFactory(), id="no_summary"),
        # reasoning
        pytest.param(QuestionDataFactory(reasoning=None),id="null_reasoning"),
        pytest.param(QuestionDataWithoutReasoningFactory(), id="no_reasoning"),
        # reasoning.status
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(status=123)), id="incorrect_reasoning_status_type"),
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(status=None)), id="null_reasoning_status"),
        pytest.param(QuestionDataWithoutReasoningStatusFactory(), id="no_reasoning_status"),
        # reasoning.worksheet_path
        pytest.param(QuestionDataFactory(reasoning=ReasoningDataFactory(worksheet_path=123)), id="incorrect_worksheet_path_type"),
        # knowledge.type
        pytest.param(QuestionDataFactory(knowledge=KnowledgeDataFactory(type=123)), id="incorrect_knowledge_type_type_when_knowledge_present"),
        pytest.param(QuestionDataFactory(knowledge=KnowledgeDataFactory(type=None)), id="null_knowledge_type_when_knowledge_present"),
        pytest.param(QuestionDataWithoutKnowledgeTypeFactory(), id="no_knowledge_type_when_knowledge_present"),
        # knowledge.path
        pytest.param(QuestionDataFactory(knowledge=KnowledgeDataFactory(path=123)), id="incorrect_knowledge_path_type_when_knowledge_present"),
        pytest.param(QuestionDataFactory(knowledge=KnowledgeDataFactory(path=None)), id="null_knowledge_path_when_knowledge_present"),
        pytest.param(QuestionDataWithoutKnowledgePathFactory(), id="no_knowledge_path_when_knowledge_present"),
        # prerequisites
        pytest.param(QuestionDataFactory(prerequisites=[1,2]), id="incorrect_prerequisite_list_types"),
        pytest.param(QuestionDataFactory(prerequisites=1), id="incorrect_prerequisite_type"),
        pytest.param(QuestionDataFactory(prerequisites=[1, "a"]), id="mixed_prerequisite_list_types"),
    ],
)

def test_QuestionData_rejects_invalid_data(data):
    with pytest.raises(ValidationError):
        QuestionData.model_validate(data)

def test_QuestionData_raises_ValidationError_on_extra_fields():
    data = QuestionDataFactory()
    data["extra_field"] = 33

    with pytest.raises(ValidationError):
            QuestionData.model_validate(data)