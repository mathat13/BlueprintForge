import pytest
from pydantic import ValidationError

from blueprint_forge import (
    GraphvizService,
    QuestionService,
)

#--- Happy Paths

def test_GraphvizService_generates_dot_file_on_valid_data(tmp_path):
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
