
from pathlib import Path

from blueprint_forge.domain.question import Question
from blueprint_forge.domain.question_collection import QuestionCollection

from blueprint_forge.infrastructure.yaml_parser import YAMLParser

from blueprint_forge.application.question.inputs import QuestionData
from blueprint_forge.application.exceptions.application_exceptions import InvalidQuestionSourceData

class QuestionService:
    @staticmethod
    def load(
            yaml_path: Path,
        ) -> QuestionCollection:
            
            # Parse YAML to dict
            data = YAMLParser.parse(yaml_path)

            # Validate returned data
            if (
                not isinstance(data, dict)
                or not isinstance(data.get("questions"), dict)
                or not data["questions"]
            ):
                raise InvalidQuestionSourceData(received=data)

            question_dict = data["questions"]
            questions = []
    
            for question_id, question_data in question_dict.items():
                
                # Validate question_data
                validated_data = QuestionData.model_validate(question_data)
    
                # Request domain object instantiation and append to list if successful
                questions.append(
                    Question.from_dict(
                        id=question_id,
                        data=validated_data.model_dump(),
                    )
                )
    
            # Validate question relationships
            question_collection = QuestionCollection(questions=questions)
                
            return question_collection