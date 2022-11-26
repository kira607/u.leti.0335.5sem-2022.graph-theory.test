from dataclasses import dataclass, field
from typing import List, Optional

from .edge import Edge
from .vertex import Vertex


@dataclass
class Graph:
    vertices: List[Vertex] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    directional: bool = False
    label: str = 'G'

    def get_edge(self, v1: str, v2: str, strict_direction: bool = False) -> Optional[Edge]:
        f, b = (v1, v2), (v2, v1)
        for e in self.edges:
            en = (e.v1.name, e.v2.name)
            if en == f:
                return e
            if en == b and not strict_direction:
                return e
        return None

    @property
    def dot(self):
        name = 'graph' if not self.directional else 'digraph'
        dot = f'{name} {self.label} {{\n'

        for edge in self.edges:
            dot += f'    {edge.dot}\n'
        
        dot += '}'

        return dot

    def __len__(self):
        return len(self.vertices)

    def __iter__(self):
        return iter(self.vertices)

    def __getitem__(self, name: str) -> Optional[Vertex]:
        for v in self:
            if v.name == name:
                return v
        return None

