from typing import Any, List, Set

from .graph import Graph
from .infinity import inf, InfNum


def get_adjacency_matrix(graph: Graph, no_path: Any, self_cross: Any) -> List[List[InfNum]]:
    # Получение матрицы смежности
    adjacency_matrix = [[None for _ in range(len(graph))] for _ in range(len(graph))]
    
    for row, v1 in enumerate(graph.vertices):
        for col, v2 in enumerate(graph.vertices):
            edge = graph.get_edge(v1.name, v2.name, strict_direction=False)

            if edge is None:
                val = self_cross if row == col else no_path
                adjacency_matrix[row][col] = val
                continue

            adjacency_matrix[row][col] = edge.weight if edge.weight is not None else 1
    
    return adjacency_matrix


def get_vertices_names(graph: Graph) -> List[str]:
    return [v.name for v in graph.vertices]


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