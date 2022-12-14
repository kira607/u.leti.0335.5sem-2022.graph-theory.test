from typing import Any, List, Set, Iterable

from dot2tex import dot2tex

from .graph import Graph
from .infinity import inf, InfNum
from .types import StrConvertable


def mkg(vertices: Iterable[StrConvertable] = (), edges: Iterable[tuple[StrConvertable, StrConvertable]] = (), label: str = 'G'):
    graph = Graph(label)
    for vertex in vertices:
        graph.add_vertex(vertex)
    for edge in edges:
        graph.add_edge(*edge)
    return graph


def get_vertices_names(graph: Graph) -> List[str]:
    return [v.name for v in graph.vertices]


def get_latex_tikz_string(graph: Graph):
    return dot2tex(graph.dot, figonly=True, usepdflatex=True, format='tikz')
