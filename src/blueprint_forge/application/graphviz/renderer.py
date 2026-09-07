from dataclasses import dataclass

from blueprint_forge.representation.graphviz.graph import GraphvizGraph
from blueprint_forge.representation.graphviz.config import GraphvizConfig

class GraphvizRenderer:
    @staticmethod
    def render(
        graph: GraphvizGraph,
        config: GraphvizConfig,
    ) -> str:
        rendered_graph = []

        rendered_graph.append(config.header)

        for node in graph.nodes:
            rendered_graph.append(node.to_graphviz())

        for edge in graph.edges:
            rendered_graph.append(edge.to_graphviz())

        rendered_graph.append(config.footer)

        return "\n".join(rendered_graph)
