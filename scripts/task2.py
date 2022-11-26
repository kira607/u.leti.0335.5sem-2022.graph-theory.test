from graph import Vertex, Edge, Graph
from base_task import BaseTask


def prefix(vertex: Vertex):
    return vertex.name[:-1]


def suffix(vertex: Vertex):
    return vertex.name[1:]


def word(edge: Edge):
    return edge.v1.name[0] + suffix(edge.v1) + edge.v2.name[-1]


class Task2(BaseTask):
    def _solve(self) -> None:
        vertices = [Vertex(name) for name in 'KQS, QSU, UQS, SQU, SUQ, QSQ, QUQ, UQU'.split(', ')]
        edges = []

        for v1 in vertices:
            for v2 in vertices:
                if v1 == v2 or suffix(v1) != prefix(v2):
                    continue
                new_edge = Edge(v1, v2, directional=True)
                new_edge.set_dot_attributes({'label': word(new_edge)})
                edges.append(new_edge)

        g = Graph(vertices, edges, directional=True)
        print('resulting graph:')
        print(g.dot)
        print('words: ')
        print(',\n'.join(word(edge) for edge in g.edges), '.', sep='')


def solve() -> None:
    Task2(2).solve()
