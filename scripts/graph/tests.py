import pytest

from .graph import Graph
from .helpers import mkg
from .algorithms import ChromaticPolynomCreator, is_full, is_null, get_adjacent_vertices, is_tree


@pytest.mark.parametrize(
    'graph, expected',
    (
        (mkg(['A']), True),
        (mkg(['A', 'B', 'C']), True),
        (mkg(edges=[('A', 'B')]), False),
    ),
)
def test_is_null(graph, expected):
    graph_is_null = is_null(graph)
    assert graph_is_null == expected


@pytest.mark.parametrize(
    'graph, expected',
    (
        (mkg(['A']), True),
        (mkg(['A', 'B', 'C']), False),
        (mkg(edges=[('A', 'B')]), True),
    ),
)
def test_is_full(graph, expected):
    graph_is_full = is_full(graph)
    assert graph_is_full == expected


@pytest.mark.parametrize(
    'graph, v1, v2, expected_vertices, expected_edges',
    (
        (
            mkg(edges=[('a', 'b')]),
            'a', 'b',
            {'a'},
            set(),
        ),
        (
            mkg(edges=[('a', 'b')]),
            'b', 'a',
            {'a'},
            set(),
        ),
        (
            mkg(edges=[('a', 'b'), ('c', 'd')]),
            'a', 'b',
            {'a', 'c', 'd'},
            {('c', 'd')},
        ),
        (
            mkg(edges=[('a', 'b'), ('a', 'c'), ('a', 'd')]),
            'a', 'c',
            {'a', 'b', 'd'},
            {('a', 'b'), ('a', 'd')},
        ),
        (
            mkg(['a', 'b', 'c', 'd'], [('c', 'd')]),
            'c', 'd',
            {'a', 'b', 'c'},
            set(),
        ),
        (
            mkg(['a', 'b', 'c'], [('a', 'b'), ('b', 'c')]),
            'a', 'b',
            {'a', 'c'},
            {('a', 'c')},
        ),
        (
            mkg(['a', 'b', 'c'], [('a', 'b'), ('b', 'c')]),
            'b', 'c',
            {'a', 'b'},
            {('a', 'b')},
        ),
        (
            mkg(edges=[('a', 'b'), ('b', 'c'), ('b', 'd')]),
            'b', 'd',
            {'a', 'b', 'c'},
            {('a', 'b'), ('b', 'c')},
        ),
        (
            mkg(edges=[('a', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'd')]),
            'b', 'd',
            {'a', 'b', 'c'},
            {('a', 'b'), ('b', 'c')},
        ),
    ),
)
def test_merge_edge(graph: Graph, v1, v2, expected_vertices, expected_edges):
    graph.merge_edge(v1, v2)

    assert set(graph._vertices.keys()) == expected_vertices
    for expected_vertex in expected_vertices:
        assert graph.get_vertex(expected_vertex).name == expected_vertex

    assert set(graph._edges.keys()) == expected_edges
    for expected_edge in expected_edges:
        assert (
            graph.get_edge(*expected_edge).v1.name == expected_edge[0] and
            graph.get_edge(*expected_edge).v2.name == expected_edge[1]
        )


@pytest.mark.parametrize(
    'graph, strategy, expected_polynom',
    (
        (mkg(['A']), None, 'K_{1}'),
        (mkg(['A']), 'O', 'O_{1}'),
        (mkg(['A', 'B']), None, 'K_{2} + K_{1}'),
        (mkg(['A', 'B']), 'O', 'O_{2}'),
        (mkg(edges=[('A', 'B')]), None, 'K_{2}'),
        (mkg(edges=[('A', 'B')]), 'O', 'O_{2} + (-1.0) * O_{1}'),
        (
            mkg(edges=[('A', 'B'), ('A', 'D'), ('A', 'C'), ('C', 'D')]),
            'O',
            'O_{4} + (-4.0) * O_{3} + (5.0) * O_{2} + (-2.0) * O_{1}',
        )
    ),
)
def test_get_chromatic_polynom(graph: Graph, strategy, expected_polynom) -> None:
    chromatic_polynom = ChromaticPolynomCreator.get_chromatic_polynom(graph, strategy)
    assert chromatic_polynom == expected_polynom


@pytest.mark.parametrize(
    'graph, target_vertex, expected_vertices',
    (
        (mkg(edges=[('a', 'b'), ('b', 'c'), ('a', 'c')]), 'a', {'b', 'c'}),
        (mkg(['d'], [('a', 'b'), ('b', 'c'), ('a', 'c')]), 'd', set()),
        (mkg(edges=[('a', 'b'), ('a', 'c'), ('a', 'd'), ('e', 'a')]), 'a', {'b', 'c', 'd', 'e'}),
        (mkg(edges=[('a', 'b'), ('a', 'c'), ('a', 'd'), ('e', 'a')]), 'e', {'a'}),
    ),
)
def test_get_adjacent_vertices(graph: Graph, target_vertex: str, expected_vertices: set[str]):
    adjacent_vertices = get_adjacent_vertices(graph, graph.get_vertex(target_vertex))
    assert {v.name for v in adjacent_vertices} == expected_vertices


@pytest.mark.parametrize(
    'graph, expected',
    (
        (mkg(), True),
        (mkg(['a']), True),
        (mkg(edges=[('a', 'b')]), True),
        (mkg(edges=[('a', 'b'), ('b', 'c'), ('a', 'c')]), False),
        (mkg(['d'], [('a', 'b'), ('b', 'c'), ('a', 'c')]), False),
        (mkg(edges=[('a', 'b'), ('a', 'c'), ('a', 'd'), ('e', 'a')]), True),
        (mkg(edges=[('a', 'b'), ('a', 'c'), ('b', 'd'), ('b', 'e'), ('c', 'f')]), True),
        (mkg(edges=[('a', 'b'), ('a', 'c'), ('b', 'd'), ('b', 'e'), ('c', 'b')]), False),
        (mkg(['z'], [('a', 'b'), ('a', 'c'), ('b', 'd'), ('b', 'e'), ('c', 'f')]), False),
    ),
)
def test_is_tree(graph: Graph, expected: bool) -> None:
    graph_is_tree = is_tree(graph)
    assert graph_is_tree == expected
