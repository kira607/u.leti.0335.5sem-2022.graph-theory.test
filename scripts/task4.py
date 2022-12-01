from base_task import BaseTask
from graph.algorithms import PruferCodeCreator
from graph.helpers import mkg, get_latex_tikz_string
from scripts.graph import Graph, Vertex


class Task4(BaseTask):
    def _solve(self) -> None:
        g = mkg(edges=[
            (3, 4),
            (4, 5),
            (5, 6),
            (1, 7),
            (1, 8),
            (1, 9),
            (2, 9),
            (2, 10),
            (5, 10),
            (10, 11),
        ])

        for vertex in g:
            vertex.set_dot_attributes({'shape': 'box'})

        root_vertex = g.get_vertex(5)
        root_vertex.update_dot_attributes({'color': 'blue'})

        for i, (graph, code, m, p) in enumerate(self._gen_prufer_code_solution(g, root_vertex), start=1):
            print(f'\\textbf{{Шаг {i}}}\n')
            print('Граф:')
            print(get_latex_tikz_string(graph))
            print(f'Лист дерева с минимальным номером: {m.name}\n')
            print(f'Добавляем номер родителя минимального листа в код и убираем минимальный лист из графа.\n')
            print(f'Код: {", ".join([str(c) for c in code])}\n')

    def _gen_prufer_code_solution(self, graph: Graph, root: Vertex):
        cls = PruferCodeCreator
        graph = graph.copy()
        code_len = len(graph) - 2
        code = []
        while len(code) < code_len:
            leafs = cls.get_graph_leaves(graph, root, root)
            min_leaf = min(leafs, key=lambda leaf: int(leaf.name))
            min_leaf.update_dot_attributes({'color': 'red'})
            parent = cls.get_parent(graph, root, min_leaf)
            parent.update_dot_attributes({'color': 'green'})
            code.append(int(parent.name))

            yield graph, code, min_leaf, parent

            graph.remove_edge(parent.name, min_leaf.name)
            graph.remove_vertex(min_leaf.name)
            parent.update_dot_attributes({'color': 'black'})
            root.update_dot_attributes({'color': 'blue'})

        return code


def solve() -> None:
    Task4(4).solve()


if __name__ == '__main__':
    solve()
