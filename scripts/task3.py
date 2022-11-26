from graph import Vertex as Vertex, Edge as Edge, Graph as Graph
from base_task import BaseTask


class Task3(BaseTask):
    def _solve(self) -> None:
        g = Graph([Vertex(x) for x in 'ABCDEFGHIJKL'])
        g.edges = [
            Edge(g['A'], g['B']),
            Edge(g['B'], g['D']),
            Edge(g['C'], g['D']),
            Edge(g['D'], g['E']),
            Edge(g['C'], g['H']),
            Edge(g['D'], g['H']),
            Edge(g['E'], g['I']),
            Edge(g['E'], g['J']),
            Edge(g['F'], g['J']),
            Edge(g['G'], g['H']),
            Edge(g['H'], g['I']),
            Edge(g['H'], g['K']),
            Edge(g['I'], g['K']),
            Edge(g['K'], g['L']),
        ]
        print(g.dot)

    def get_chromatic_polynom(self, graph):
        pass


def solve() -> None:
    Task3(3).solve()
