from typing import Any, List, Set, Optional, Iterable

from .graph import Graph
from .helpers import mkg
from .infinity import inf, InfNum
from .polynom.polynom import Polynom, PolyToken
from .vertex import Vertex


def get_adjacency_matrix(graph: Graph, no_path: Any, self_cross: Any) -> List[List[InfNum]]:
    '''
    Get a graph adjacency matrix.

    :param graph: Target graph.
    :param no_path: A value to be put in matrix if there is no edge connecting vertices.
    :param self_cross: A value to be put in matrix for self-crossing vertices (if there is no cycle edge).

    :return: Target graph adjacency matrix
    '''
    adjacency_matrix = [[None for _ in range(len(graph))] for _ in range(len(graph))]

    for row, v1 in enumerate(graph.vertices):
        for col, v2 in enumerate(graph.vertices):
            edge = graph.get_edge(v1.name, v2.name, default=None)

            if edge is None:
                val = self_cross if row == col else no_path
                adjacency_matrix[row][col] = val
                continue

            adjacency_matrix[row][col] = edge.weight if edge.weight is not None else 1

    return adjacency_matrix


def get_floyd_matrix(graph: Graph):
    # Алгоритм Флойда-Уоршелла

    n = len(graph)
    d = get_adjacency_matrix(graph, inf, 0)

    for k in range(n):
        for j in range(n):
            for i in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])

    return d


def get_eccentricities(graph: Graph) -> list[int]:
    # Нахождение эксцентриситетов

    n = len(graph)
    d = get_floyd_matrix(graph)

    e = []

    for row in range(n):
        e.append(max(d[row]))

    return e


def get_radius(graph: Graph) -> int:
    eccentricities = get_eccentricities(graph)
    radius = min(eccentricities)
    return radius


def get_diameter(graph: Graph) -> int:
    eccentricities = get_eccentricities(graph)
    diameter = max(eccentricities)
    return diameter


def get_centers(graph: Graph) -> Set[str]:
    eccentricities = get_eccentricities(graph)
    radius = get_radius(graph)
    centers = set()

    for i, e in enumerate(eccentricities):
        if e == radius:
            centers.add(graph.vertices[i].name)

    return centers


def is_null(graph: Graph) -> bool:
    return not bool(len(graph.edges))


def get_number_of_edges_to_be_full(graph: Graph) -> int:
    n = len(graph)
    return int((n * (n - 1)) / 2)


def is_full(graph: Graph) -> bool:
    return len(graph.edges) == get_number_of_edges_to_be_full(graph)


def get_adjacent_vertices(graph: Graph, vertex: Vertex) -> List[Vertex]:
    adjacent_vertices = []
    for v in graph:
        e = graph.get_edge(vertex.name, v.name, default=None)
        if e is None:
            continue
        if e.v1 == vertex:
            adjacent_vertices.append(e.v2)
        elif e.v2 == vertex:
            adjacent_vertices.append(e.v1)
    return adjacent_vertices


def get_not_adjacent_vertices(graph: Graph) -> list[tuple[str, str]]:
    not_adjacent_vertices = []
    for v1 in graph:
        for v2 in graph:
            if graph.get_edge(v1.name, v2.name, default=None):
                continue
            if v1 == v2:
                continue
            not_adjacent_vertices.append((v1.name, v2.name))
    return not_adjacent_vertices


class ChromaticPolynomCreator:

    @classmethod
    def pick_optimal_strategy(cls, graph: Graph):
        n = len(graph)
        if get_number_of_edges_to_be_full(graph) / 2 > n:
            strategy = 'O'
        else:
            strategy = 'K'
        return strategy

    @classmethod
    def get_chromatic_polynom(cls, graph: Graph, strategy=None) -> str:
        poly = cls._get_chromatic_polynom(graph, strategy)
        return str(poly)

    @classmethod
    def _get_chromatic_polynom(cls, graph: Graph, strategy=None) -> Polynom:
        n = len(graph)
        strategy = strategy or cls.pick_optimal_strategy(graph)

        if strategy == 'O':
            if is_null(graph):
                return Polynom.from_tokens(PolyToken(f'O_{{{n}}}'))
            return cls.o_strategy(graph)

        if strategy == 'K':
            if is_full(graph):
                return Polynom.from_tokens(PolyToken(f'K_{{{n}}}'))
            return cls.k_strategy(graph)

    @classmethod
    def o_strategy(cls, graph: Graph) -> Polynom:
        '''to O : P(G_1, x) = P(G, x) - P(G_2, x)'''
        next_strategy = 'O'

        g = graph.copy()
        target_edge = g.edges[0].v1.name, g.edges[0].v2.name
        g.remove_edge(*target_edge)
        g2 = graph.copy()
        g2.merge_edge(*target_edge)

        left = cls._get_chromatic_polynom(g, next_strategy)
        right = cls._get_chromatic_polynom(g2, next_strategy)
        return left - right

    @classmethod
    def k_strategy(cls, graph: Graph) -> Polynom:
        '''to K : P(G, x) = P(G_1, x) + P(G_2, x)'''
        next_strategy = 'K'

        v1, v2 = get_not_adjacent_vertices(graph)[0]
        g1 = graph.copy()
        g1.add_edge(v1, v2)
        g2 = g1.copy()
        g2.merge_edge(v1, v2)

        left = cls._get_chromatic_polynom(g1, next_strategy)
        right = cls._get_chromatic_polynom(g2, next_strategy)
        return left + right


def is_cycled(
    graph: Graph,
    current_vertex: Vertex,
    visited: dict[Vertex, bool],
    parent_vertex: Optional[Vertex] = None
) -> bool:
    visited[current_vertex] = True

    adjacent_vertices = get_adjacent_vertices(graph, current_vertex)
    for adjacent_vertex in adjacent_vertices:
        if not visited.get(adjacent_vertex):
            if is_cycled(graph, adjacent_vertex, visited, current_vertex):
                return True
        elif adjacent_vertex != parent_vertex:
            return True

    return False


def is_tree(graph: Graph) -> bool:
    if len(graph) <= 2:
        return True

    visited = {vertex: False for vertex in graph.vertices}

    if is_cycled(graph, graph.vertices[0], visited):
        return False

    # make sure that all vertices are visited
    return all(visited.values())


class TreeNode:
    def __init__(self, number: int, parent: 'TreeNode' = None, children: list['TreeNode'] = None):
        self.number = number
        self.parent = parent
        self.children = children or []

    def get_leaves(self, collected=None):
        if not self.children:
            return [self]

        collected = collected or []

        for child in self.children:
            collected += child.get_leaves(collected)

        return collected


def graph_to_tree(graph: Graph, root: Vertex) -> TreeNode:
    if not is_tree(graph):
        raise ValueError(f'Graph is not a tree: {repr(graph)}')

    tree = TreeNode(int(root.name))
    stack = [(tree, root)]
    while stack:
        node, vertex = stack.pop()
        children = get_adjacent_vertices(graph, vertex)
        if node.parent:
            children.remove(graph.get_vertex(str(node.parent.number)))
        for child_vertex in children:
            child_node = TreeNode(int(child_vertex.name), node)
            node.children.append(child_node)
            stack.append((child_node, child_vertex))

    return tree


def tree_to_dot(tree: TreeNode):
    edges = _tree_to_dot(tree)
    return mkg(edges=edges).dot


def _tree_to_dot(tree: TreeNode, collected=None):
    if not tree.children:
        return []

    collected = collected or []

    for child in tree.children:
        collected.append((tree.number, child.number))
        collected.extend(_tree_to_dot(child))

    return collected


def get_prufer_code(graph: Graph, root: Vertex) -> list[int]:
    tree = graph_to_tree(graph, root)
    code = []
    while len(code) < len(graph) - 2:
        leafs = tree.get_leaves()
        min_leaf = min(leafs, key=lambda leaf: leaf.number)
        parent = min_leaf.parent
        code.append(parent.number)
        parent.children.remove(min_leaf)

    return code


class PruferCodeCreator:

    @classmethod
    def get_prufer_code(cls, graph: Graph, root: Vertex) -> list[int]:
        graph = graph.copy()
        code_len = len(graph) - 2
        code = []
        while len(code) < code_len:
            leafs = cls.get_graph_leaves(graph, root, root)
            min_leaf = min(leafs, key=lambda leaf: int(leaf.name))
            parent = cls.get_parent(graph, root, min_leaf)
            code.append(int(parent.name))

            graph.remove_edge(parent.name, min_leaf.name)
            graph.remove_vertex(min_leaf.name)

        return code

    @classmethod
    def get_graph_leaves(cls, graph: Graph, root: Vertex, vertex: Vertex, collected=None) -> list[Vertex]:
        children = cls.get_children(graph, root, vertex)
        if not children:
            return [vertex]

        collected = collected or []

        for child in children:
            collected += cls.get_graph_leaves(graph, root, child, collected)

        return collected

    @classmethod
    def get_children(cls, graph: Graph, root: Vertex, vertex: Vertex) -> list[Vertex]:
        adjacent = get_adjacent_vertices(graph, vertex)
        parent = cls.get_parent(graph, root, vertex)
        if parent:
            adjacent.remove(parent)
        return adjacent

    @classmethod
    def get_parent(cls, graph: Graph, root: Vertex, vertex: Vertex) -> Optional[Vertex]:
        if root == vertex:
            return None

        adjacent_vertices = get_adjacent_vertices(graph, vertex)
        min_dist = 999999999
        parent = None
        for v in adjacent_vertices:
            d = cls.get_root_distance(graph, root, v)
            if d <= min_dist:
                min_dist = d
                parent = v
        return parent

    @classmethod
    def get_root_distance(cls, graph: Graph, root: Vertex, vertex: Vertex) -> int:
        distance = 0
        if root == vertex:
            return distance
        previous_layer = [(None, root)]
        while True:
            distance += 1

            this_layer = []

            for parent, v in previous_layer:
                children = get_adjacent_vertices(graph, v)
                if parent in children:
                    children.remove(parent)
                this_layer.extend([(v, child) for child in children])

            for _, child in this_layer:
                if child == vertex:
                    return distance

            previous_layer = this_layer


def graph_from_prufer_code(code: list[int]) -> Graph:
    available_vertices = [i for i in range(1, len(code) + 3)]
    edges = []
    for i, v1 in enumerate(code):
        left_in_code = code[i:]
        not_in_code = [v for v in available_vertices if v not in left_in_code]
        v2 = min(not_in_code)
        available_vertices.remove(v2)
        edges.append((str(v1), str(v2)))
    edges.append((str(available_vertices[0]), str(available_vertices[1])))

    return mkg(edges=edges)
