import pytest
from pydantic import ValidationError

from blueprint_forge import (
    QuestionService,
    InvalidQuestionID,
    InvalidPrerequisites,
    YAMLFileNotFound,
)

def test_QuestionService_load_handles_valid_source_data(tmp_path):
    # Setup
        yaml_path = tmp_path / "questions.yaml"
    
        yaml_path.write_text(
            """
            questions:
              node_1:
                question: "What is engineering information?"
                summary: "Test summary"
                reasoning:
                  status: "complete"
                  worksheet_path: "reasoning/test.md"
                knowledge:
                  type: "adr"
                  path: "knowledge/test.md"
                prerequisites: []
    
              node_2:
                question: "What is an ADR?"
                summary: "Test summary"
                reasoning:
                  status: "complete"
                  worksheet_path: "reasoning/test2.md"
                knowledge:
                  type: "adr"
                  path: "knowledge/test2.md"
                prerequisites:
                  - node_1
            """
        )

        service = QuestionService()

        # Execution
        question_collection = service.load(
            yaml_path=yaml_path,
        )

        # Validation
        assert {q.id for q in question_collection.questions} == {
            "node_1",
            "node_2",
        }

def test_QuestionService_load_handles_invalid_QuestionData(tmp_path):
    # Setup
        yaml_path = tmp_path / "questions.yaml"
    
        yaml_path.write_text(
            """
            questions:
              node_1:
                question: 123
                summary: "Test summary"
                reasoning:
                    status: "complete"
                    worksheet_path: "reasoning/test.md"
                knowledge:
                    type: "adr"
                    path: "knowledge/test.md"
                prerequisites: []
            """
        ) # Invalid question field type will trigger QuestionData exception


        service = QuestionService()

        # Validation
        with pytest.raises(ValidationError):
            service.load(
                   yaml_path=yaml_path,
                   )

def test_QuestionService_load_handles_invalid_Question(tmp_path):
    # Setup
        yaml_path = tmp_path / "questions.yaml"
    
        yaml_path.write_text(
            """
            questions:
              123:
                question: "What is engineering information?"
                summary: "Test summary"
                reasoning:
                    status: "complete"
                    worksheet_path: "reasoning/test.md"
                knowledge:
                    type: "adr"
                    path: "knowledge/test.md"
                prerequisites: []
            """
        ) # Invalid question id will trigger Question exception


        service = QuestionService()

        # Validation
        with pytest.raises(InvalidQuestionID):
            service.load(
                   yaml_path=yaml_path,
                   )

def test_QuestionService_load_handles_invalid_QuestionCollection(tmp_path):
    # Setup
        yaml_path = tmp_path / "questions.yaml"
    
        yaml_path.write_text(
            """
            questions:
              node_1:
                question: "What is engineering information?"
                summary: "Test summary"
                reasoning:
                  status: "complete"
                  worksheet_path: "reasoning/test.md"
                knowledge:
                  type: "adr"
                  path: "knowledge/test.md"
                prerequisites: []
    
              node_2:
                question: "What is an ADR?"
                summary: "Test summary"
                reasoning:
                  status: "complete"
                  worksheet_path: "reasoning/test2.md"
                knowledge:
                  type: "adr"
                  path: "knowledge/test2.md"
                prerequisites:
                  - node_3
            """
        ) # Invalid prerequisites on node_2 will trigger QuestionCollection exception


        service = QuestionService()

        # Validation
        with pytest.raises(InvalidPrerequisites):
            service.load(
                   yaml_path=yaml_path,
                   )     
        
def test_QuestionService_load_handles_YAMLParser_exception(tmp_path):
    # Setup
        yaml_path = tmp_path / "questions.yaml"
        # Path not defined raises YAMLParser exception

        service = QuestionService()

        # Validation
        with pytest.raises(YAMLFileNotFound):
            service.load(
                   yaml_path=yaml_path,
            )