from copy import deepcopy
from typing import Any, Optional

from .edge import Edge
from .missing import MISSING
from .types import StrConvertable
from .vertex import Vertex


class Graph:
    '''
    A class representing a non-directional graph.

    Stores graph as a collection of vertices and edges
    '''

    _dot_name = 'graph'

    def __init__(self, label: str = 'G'):
        self._label = label
        self._vertices: dict[str, Vertex] = {}
        self._edges: dict[tuple[str, str], Edge] = {}

    def __len__(self):
        return len(self._vertices)

    def __iter__(self):
        return iter(self._vertices.values())

    def __repr__(self):
        return f'<{self.__class__.__name__} {repr(set(self._vertices.keys()))}, {repr(set(self._edges.keys()))}>'

    @property
    def label(self) -> str:
        return self._label

    @property
    def vertices(self) -> tuple[Vertex, ...]:
        return tuple(self._vertices.values())

    @property
    def edges(self) -> tuple[Edge]:
        return tuple(self._edges.values())

    def get_vertex(self, vertex_name: StrConvertable, default: Any = MISSING) -> Vertex:
        vertex_name = str(vertex_name)
        v = self._vertices.get(vertex_name, default)
        if v is MISSING:
            raise KeyError(f'Vertex {vertex_name} is not present in the graph.')
        return v

    def add_vertex(self, name: StrConvertable) -> Vertex:
        name = str(name)
        existing = self._vertices.get(name)
        if existing:
            return existing
        vertex = Vertex(name)
        self._vertices[name] = vertex
        return vertex

    def remove_vertex(self, name: StrConvertable) -> None:
        name = str(name)
        exists = self._vertices.get(name, MISSING)
        if exists is MISSING:
            return
        del self._vertices[name]

    def get_edge(self, v1: StrConvertable, v2: StrConvertable, default: Any = MISSING) -> Edge:
        key = self._get_edge_key(v1, v2)

        if key:
            return self._edges[key]
        elif default is MISSING:
            raise KeyError(f'Edge ({v1}, {v2}) is not present in the graph: {repr(self)}.')
        else:
            return default

    def add_edge(self, v1: StrConvertable, v2: StrConvertable) -> Edge:
        v1, v2 = self.add_vertex(v1), self.add_vertex(v2)
        key = (v1.name, v2.name)
        existing = self.get_edge(*key, default=None)
        if existing:
            return existing
        edge = Edge(v1, v2)
        self._edges[key] = edge
        return edge

    def remove_edge(self, v1: StrConvertable, v2: StrConvertable) -> None:
        key = self._get_edge_key(v1, v2)
        exists = self.get_edge(*key)

        if exists is MISSING:
            raise RuntimeError(f'Could not find edge {key} in {self.dot}')

        del self._edges[key]

    def merge_edge(self, v1: str, v2: str) -> None:
        '''
        Merge edge (l, r).

        Removes (l, r) edge and ``r`` vertex.
        All edges connected to ``r`` are reconnected to ``l``.
        '''
        merge_edge = self.get_edge(v1, v2, default=None)
        if not merge_edge:
            return
        v1, v2 = merge_edge.v1, merge_edge.v2

        for edge in self.edges:
            if edge == merge_edge:
                continue
            if edge.v1 == v2:
                edge.v1 = v1
                self.remove_edge(v2.name, edge.v2.name)
                self.add_edge(v1.name, edge.v2.name)
            if edge.v2 == v2:
                self.remove_edge(edge.v1.name, v2.name)
                self.add_edge(edge.v1.name, v1.name)

        self.remove_edge(v1.name, v2.name)
        self.remove_vertex(v2.name)

    def copy(self) -> 'Graph':
        return deepcopy(self)

    @property
    def dot(self):
        name = self._dot_name
        dot = f'{name} {self.label} {{\n'

        for vertex in self.vertices:
            dot += f'    {vertex.dot}\n'

        for edge in self.edges:
            dot += f'    {edge.dot}\n'
        
        dot += '}'

        return dot

    def _get_edge_key(self, v1: StrConvertable, v2: StrConvertable) -> Optional[tuple[str, str]]:
        v1, v2 = str(v1), str(v2)
        if self._edges.get((v1, v2), None):
            return v1, v2
        elif self._edges.get((v2, v1), None):
            return v2, v1
        else:
            return None
