from typing import Any, List, Set, Iterable

from .graph import Graph
from .infinity import inf, InfNum


def mkg(vertices: Iterable[str] = (), edges: Iterable[tuple[str, str]] = ()):
    graph = Graph()
    for vertex in vertices:
        graph.add_vertex(vertex)
    for edge in edges:
        graph.add_edge(*edge)
    return graph


def get_vertices_names(graph: Graph) -> List[str]:
    return [v.name for v in graph.vertices]
