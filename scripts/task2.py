import dataclasses

from typing import Optional

import graphviz


@dataclasses.dataclass
class Vertex:
    name: str

    @property
    def prefix(self):
        return self.name[:-1]

    @property
    def suffix(self):
        return self.name[1:]


@dataclasses.dataclass
class Edge:
    source: Vertex
    dest: Vertex
    
    @property
    def word(self):
        return self.source.name[0] + self.source.suffix + self.dest.name[-1]


def check_merge(v1: Vertex, v2: Vertex) -> Optional[str]:
    return None


def solve():

    v = Vertex('ABC')
    print(v, v.prefix, v.suffix)

    vertices = [Vertex(name) for name in 'KQS, QSU, UQS, SQU, SUQ, QSQ, QUQ, UQU'.split(', ')]

    edges = []

    for v1 in vertices:
        for v2 in vertices:
            if v1 == v2:
                continue
            if v1.suffix != v2.prefix:
                continue
            edges.append(Edge(v1, v2))
    
    dot = 'digraph G {\n'
    for v in vertices:
        dot += f'    {v.name}\n'

    for edge in edges:
        dot += f'    {edge.source.name} -> {edge.dest.name} [label={edge.word}]\n'

    dot += '}'

    print(dot)

