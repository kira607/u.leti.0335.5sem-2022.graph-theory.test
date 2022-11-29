from copy import deepcopy
from typing import Any, Optional

from .missing import MISSING
from .edge import Edge
from .vertex import Vertex


class Graph:
    '''
    A class representing a graph.

    Stores graph as a collection of vertices and edges
    '''
    def __init__(self, *edges: tuple[str, str], label: str = 'G'):
        self._label = label
        self._vertices: dict[str, Vertex] = {}
        self._edges: dict[tuple[str, str], Edge] = {}
        for v1, v2 in edges:
            self.add_edge(v1, v2)

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
    def vertices(self) -> tuple[Vertex]:
        return tuple(self._vertices.values())

    @property
    def edges(self) -> tuple[Edge]:
        return tuple(self._edges.values())

    def get_vertex(self, vertex_name: str, default: Any = MISSING) -> Vertex:
        v = self._vertices.get(vertex_name, default)
        if v is MISSING:
            raise KeyError(f'Vertex {vertex_name} is not present in the graph.')
        return v

    def add_vertex(self, name: str) -> Vertex:
        existing = self._vertices.get(name)
        if existing:
            return existing
        vertex = Vertex(name)
        self._vertices[name] = vertex
        return vertex

    def remove_vertex(self, name: str) -> None:
        exists = self._vertices.get(name, MISSING)
        if exists is MISSING:
            return
        del self._vertices[name]

    def get_edge(self, v1: str, v2: str, default: Any = MISSING) -> Edge:
        if self._edges.get((v1, v2), None):
            return self._edges[(v1, v2)]
        elif self._edges.get((v2, v1), None):
            return self._edges[(v2, v1)]
        elif default is MISSING:
            raise KeyError(f'Edge ({v1}, {v2}) is not present in the graph: {repr(self)}.')
        else:
            return default

    def add_edge(self, v1: str, v2: str) -> Edge:
        v1, v2 = self.add_vertex(v1), self.add_vertex(v2)
        key = (v1.name, v2.name)
        existing = self.get_edge(*key, default=None)
        if existing:
            return existing
        edge = Edge(v1, v2)
        self._edges[key] = edge
        return edge

    def remove_edge(self, v1: str, v2: str) -> None:
        key = v1, v2
        exists = self.get_edge(*key)
        if exists is MISSING:
            raise RuntimeError(f'Could not find edge {key} in {self.dot}')
        del self._edges[key]

    def merge_edge(self, l: str, r: str) -> None:
        '''
        Merge edge (l, r).

        Removes (l, r) edge and r vertex.
        All edges connected to ``r`` are reconnected to ``l``.
        '''
        merge_edge = self.get_edge(l, r, None)
        if not merge_edge:
            return
        l, r = merge_edge.v1, merge_edge.v2

        for edge in self.edges:
            if edge == merge_edge:
                continue
            if edge.v1 == r:
                edge.v1 = l
                self.remove_edge(r.name, edge.v2.name)
                self.add_edge(l.name, edge.v2.name)
            if edge.v2 == r:
                self.remove_edge(edge.v1.name, r.name)
                self.add_edge(edge.v1.name, l.name)

        self.remove_edge(l.name, r.name)
        self.remove_vertex(r.name)

    def copy(self) -> 'Graph':
        return deepcopy(self)

    @property
    def dot(self):
        name = 'graph'
        dot = f'{name} {self.label} {{\n'

        for vertex in self.vertices:
            dot += f'     {vertex.name}\n'

        for edge in self.edges:
            dot += f'    {edge.dot}\n'
        
        dot += '}'

        return dot
