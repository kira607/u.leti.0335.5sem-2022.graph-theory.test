from typing import Optional

from .edge import Edge
from .graph import Graph
from .types import StrConvertable


class Digraph(Graph):
    '''
    A class representing directional graph.

    Stores graph as a collection of vertices and edges.
    '''

    _dot_name = 'digraph'

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> Edge:
        edge = super().add_edge(v1, v2)
        edge.directional = True
        return edge

    def in_degree(self, vertex: StrConvertable) -> int:
        v2 = self.get_vertex(vertex)
        in_degree = 0
        for v1 in self.vertices:
            edge = self.get_edge(v1.name, v2.name, default=None)
            if not edge:
                continue
            in_degree += 1
        return in_degree

    def out_degree(self, vertex: StrConvertable) -> int:
        v1 = self.get_vertex(vertex)
        out_degree = 0
        for v2 in self.vertices:
            edge = self.get_edge(v1.name, v2.name, default=None)
            if not edge:
                continue
            out_degree += 1
        return out_degree

    def _get_edge_key(self, v1: StrConvertable, v2: StrConvertable) -> Optional[tuple[str, str]]:
        v1, v2 = str(v1), str(v2)
        if self._edges.get((v1, v2), None):
            return v1, v2
        else:
            return None
