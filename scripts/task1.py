from base_task import BaseTask
from graph.algorithms import get_radius, get_diameter, get_centers
from graph.helpers import mkg


class Task1(BaseTask):
    def _solve(self) -> None:
        g = mkg(edges=[
            ('2', '3'),
            ('4', '5'),
            ('1', '6'),
            ('2', '6'),
            ('4', '6'),
            ('4', '7'),
            ('4', '9'),
            ('5', '10'),
            ('8', '9'),
        ])

        print(g.dot)
        print(f'{get_radius(g)=}')
        print(f'{get_diameter(g)=}')
        print(f'{get_centers(g)=}')


def solve() -> None:
    Task1(1).solve()


if __name__ == '__main__':
    solve()
