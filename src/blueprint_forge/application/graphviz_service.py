from pathlib import Path

from blueprint_forge.infrastructure.file_writer import GraphvizFileWriter
from blueprint_forge.infrastructure.graphviz.config_loader import GraphvizConfigLoader
from blueprint_forge.representation.graphviz.graph import GraphvizGraph
from blueprint_forge.application.graphviz.renderer import GraphvizRenderer
from blueprint_forge.application.question_service import QuestionService

class GraphvizService:
    def __init__(self, question_service: QuestionService):
        self.question_service = question_service

    def generate(
        self,
        yaml_path: Path,
        header_path: Path,
        footer_path: Path,
        output_path: Path,
    ):
        renderer = GraphvizRenderer()

        question_collection = QuestionService.load(yaml_path=yaml_path)
            
        # Construct Graphviz representation
        graph = GraphvizGraph.from_question_collection(collection=question_collection)

        # Load rendering configuration
        config = GraphvizConfigLoader.load(
            header_path=header_path,
            footer_path=footer_path,
        )

        # Render
        rendered_graph = renderer.render(
            graph=graph,
            config=config,
        )

        # Persist
        GraphvizFileWriter.write(
            output=rendered_graph,
            path=output_path,
        )
