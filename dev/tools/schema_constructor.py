from pathlib import Path
import json

from blueprint_forge.application.question.inputs import QuestionData


def main():
    schema = QuestionData.model_json_schema()

    Path("docs/schemas/question_data.schema.json").write_text(
        json.dumps(schema, indent=2) + "\n"
    )


if __name__ == "__main__":
    main()