from base_task import BaseTask
from graph import Vertex as Vertex, Edge as Edge, Graph as Graph
from graph.helpers import get_radius, get_diameter, get_centers


class Task1(BaseTask):
    def _solve(self) -> None:
        g = Graph([Vertex(str(x)) for x in range(1, 11)])
        g.edges = [
            Edge(g['2'], g['3']),
            Edge(g['4'], g['5']),
            Edge(g['1'], g['6']),
            Edge(g['2'], g['6']),
            Edge(g['4'], g['6']),
            Edge(g['4'], g['7']),
            Edge(g['4'], g['9']),
            Edge(g['5'], g['10']),
            Edge(g['8'], g['9']),
        ]

        print(g.dot)
        print(f'{get_radius(g)=}')
        print(f'{get_diameter(g)=}')
        print(f'{get_centers(g)=}')



def solve() -> None:
    Task1(1).solve()
