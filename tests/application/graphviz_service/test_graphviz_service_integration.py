import pytest
from pydantic import ValidationError

from blueprint_forge import (
    GraphvizService,
    QuestionService,
    ConfigFileNotFound,
    InvalidQuestionID,
)

#--- Happy Paths

def test_GraphvizService_handles_valid_data(tmp_path):
    # Setup
    yaml_path = tmp_path / "questions.yaml"
    header_path = tmp_path / "header.dot"
    footer_path = tmp_path / "footer.dot"
    output_path = tmp_path / "output.dot"

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

    header_path.write_text("HEADER")
    footer_path.write_text("FOOTER")

    application = GraphvizService(question_service=QuestionService())

    # Execution
    application.generate(
        yaml_path=yaml_path,
        header_path=header_path,
        footer_path=footer_path,
        output_path=output_path,
    )

    # Validation
    assert output_path.exists()

    output = output_path.read_text()

    assert output.startswith("HEADER")
    assert output.endswith("FOOTER")

    assert "node_1" in output
    assert "node_2" in output
    assert 'label="What' in output
    assert "node_1 -> node_2" in output

#--- Unhappy paths

def test_GraphvizService_handles_QuestionService_load_failure(tmp_path):
    # Setup
    yaml_path = tmp_path / "questions.yaml"
    header_path = tmp_path / "header.dot"
    footer_path = tmp_path / "footer.dot"
    output_path = tmp_path / "output.dot"

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
    ) # Invalid ID on first question will raise exception propagated by QuestionService.load()

    header_path.write_text("HEADER")
    footer_path.write_text("FOOTER")

    application = GraphvizService(question_service=QuestionService())

    # Validation
    with pytest.raises(InvalidQuestionID):
      application.generate(
          yaml_path=yaml_path,
          header_path=header_path,
          footer_path=footer_path,
          output_path=output_path,
      )

def test_GraphvizService_handles_GraphvizConfigLoader_failure(tmp_path):
    # Setup
    yaml_path = tmp_path / "questions.yaml"
    header_path = tmp_path / "header.dot"
    footer_path = tmp_path / "footer.dot"
    output_path = tmp_path / "output.dot"

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

    # No header_path write write will raise GraphvizConfigLoader exception
    footer_path.write_text("FOOTER")

    application = GraphvizService(question_service=QuestionService())

    # Validation
    with pytest.raises(ConfigFileNotFound):
      application.generate(
          yaml_path=yaml_path,
          header_path=header_path,
          footer_path=footer_path,
          output_path=output_path,
      )