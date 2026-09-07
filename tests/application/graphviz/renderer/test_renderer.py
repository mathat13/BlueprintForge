from typing import List

from blueprint_forge import (
    Question,
    QuestionCollection,
    GraphvizRenderer,
    GraphvizConfig,
    GraphvizGraph,
)

def test_GraphVizRenderer_renders_correctly(questions: List[Question]):
    # Setup
    renderer = GraphvizRenderer()

    config = GraphvizConfig(
        header="HEADER",
        footer="FOOTER",
    )
    
    question_collection = QuestionCollection(questions=questions)
    graph = GraphvizGraph.from_question_collection(collection=question_collection)

    # Execution
    output = renderer.render(
        graph=graph,
        config=config,
        )

    # Validation
    assert isinstance(output, str)

    assert output.startswith("HEADER")
    assert output.endswith("FOOTER")

    for node in graph.nodes:
        assert node.to_graphviz() in output

    for edge in graph.edges:
        assert edge.to_graphviz() in output
