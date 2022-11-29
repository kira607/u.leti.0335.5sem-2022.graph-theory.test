from graph import Vertex, Edge, Graph
from base_task import BaseTask
from scripts.graph.helpers import mkg


def prefix(vertex: Vertex):
    return vertex.name[:-1]


def suffix(vertex: Vertex):
    return vertex.name[1:]


def word(edge: Edge):
    return edge.v1.name[0] + suffix(edge.v1) + edge.v2.name[-1]


class Task2(BaseTask):
    def _solve(self) -> None:
        g = mkg('KQS, QSU, UQS, SQU, SUQ, QSQ, QUQ, UQU'.split(', '))

        for v1 in g.vertices:
            for v2 in g.vertices:
                if v1 == v2 or suffix(v1) != prefix(v2):
                    continue
                new_edge = g.add_edge(v1, v2)
                new_edge.directional = True
                new_edge.set_dot_attributes({'label': word(new_edge)})

        print('resulting graph:')
        print(g.dot)
        print('words: ')
        print(',\n'.join(word(edge) for edge in g.edges), '.', sep='')


def solve() -> None:
    Task2(2).solve()


if __name__ == '__main__':
    solve()
