from .application.graphviz_service import GraphvizService
from .application.question_service import QuestionService
from .presentation.cli import create_cli


def create_application():
    question_service = QuestionService()
    graphviz_service = GraphvizService(
        question_service=question_service,
    )

    return create_cli(
        graphviz_service=graphviz_service,
        question_service=question_service,
    )

def main():
    app = create_application()
    app()


if __name__ == "__main__":
    main()