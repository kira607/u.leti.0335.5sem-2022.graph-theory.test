from base_task import BaseTask
from mako.template import Template

from scripts.graph.helpers import mkg, get_latex_tikz_string


class Task5(BaseTask):
    def _solve(self) -> None:
        code = [7, 3, 3, 9, 3, 4, 4, 5, 6]
        step_template = Template('''
\\textbf{Шаг} ${i}

Код: ${left_code}

Оставшиеся вершины: ${available_vertices}

Оставшиеся вершины не входящие в код: ${not_in_code}

Минимальная оставшиеся вершина не входящяя в код: ${v2}

Новое ребро для добавления: ${new_edge}

Полученные рёбра: ${edges}
        ''')

        for i, (left_code, available_vertices, not_in_code, v2, new_edge, edges) in enumerate(self._gen_graph_from_prufer_code_solution(code), start=1):
            print(step_template.render(i=i, left_code=left_code, available_vertices=available_vertices, not_in_code=not_in_code, v2=v2, new_edge=new_edge, edges=edges))

        print('Полученный граф:')

        print(get_latex_tikz_string(mkg(edges=edges)))

    def _gen_graph_from_prufer_code_solution(self, code: list[int]):
        available_vertices = [i for i in range(1, len(code) + 3)]
        edges = []
        for i, v1 in enumerate(code):
            left_in_code = code[i:]
            not_in_code = [v for v in available_vertices if v not in left_in_code]
            v2 = min(not_in_code)
            new_edge = (str(v1), str(v2))
            edges.append(new_edge)

            yield left_in_code, available_vertices, not_in_code, v2, new_edge, edges

            available_vertices.remove(v2)
        edges.append((str(available_vertices[0]), str(available_vertices[1])))
        yield [], available_vertices, available_vertices, None, (str(available_vertices[0]), str(available_vertices[1])), edges

def solve() -> None:
    Task5(5).solve()


if __name__ == '__main__':
    solve()
