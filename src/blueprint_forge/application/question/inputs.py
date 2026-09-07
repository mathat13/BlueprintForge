from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

class QuestionDataBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class ReasoningData(QuestionDataBaseModel):
    status: str = Field(
        description=("Current status of the engineering reasoning. "
                     "Must be one of: 'in_progress' or 'complete'."
        ),
        examples=["in_progress", "complete"],
    )
    worksheet_path: str | None = Field(
        default=None,
        description=(
            "Path to the worksheet containing the reasoning for this question. "
            "May be omitted when no worksheet exists."
        ),
        examples=["reasoning/worksheets/authority.md"],
    )

class KnowledgeData(QuestionDataBaseModel):
    type: str = Field(
        description=("Type of knowledge artifact produced by the question. "
                     "Must be one of: 'adr' or 'classification' if included."
        ),
        examples=["adr", "classification"],
    )

    path: str = Field(
        description="Path to the knowledge artifact.",
        examples=["knowledge/adrs/authority.md"],
    )

class QuestionData(QuestionDataBaseModel):
    question: str = Field(
        description="The question being investigated.",
        examples=[
            "What makes engineering information authoritative?"
        ],
    )

    summary: str = Field(
        description="A concise summary of the current understanding of the question.",
        examples=[
            "Defines the criteria used to determine whether engineering "
            "information is authoritative."
        ],
    )

    reasoning: ReasoningData = Field(
        description="Information describing the reasoning process for this question."
    )

    knowledge: KnowledgeData | None = Field(
        default=None,
        description=(
            "The knowledge artifact produced by the question, if one exists."
        ),
    )

    prerequisites: list[str] = Field(
        description=(
            "IDs of questions whose knowledge is required before this question "
            "can be resolved."
        ),
        examples=[
            ["engineering_information_types", "authority"]
        ],
    )