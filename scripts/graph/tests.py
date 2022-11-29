import pytest

from .graph import Graph
from .helpers import mkg
from .algorithms import ChromaticPolynomCreator, is_full, is_null


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
        (mkg(edges=[('A', 'B')]), 'O', 'O_{2} - O_{1}'),
        (
            mkg(edges=[('A', 'B'), ('A', 'D'), ('A', 'C'), ('C', 'D')]),
            'O',
            'O_{4} - O_{3} - O_{3} - O_{2} - O_{3} - O_{2} - O_{3} - O_{2} - O_{2} - O_{1} - O_{2} - O_{1}',
        )
    ),
)
def test_get_chromatic_polynom(graph: Graph, strategy, expected_polynom) -> None:
    chromatic_polynom = ChromaticPolynomCreator.get_chromatic_polynom(graph, strategy)
    assert chromatic_polynom == expected_polynom


@pytest.mark.parametrize(
    'raw_polynom, expected',
    (
        (
            [
                ChromaticPolynomCreator.PolyToken('O_{1}'),
            ],
            'O_{1}',
        ),
        (
            [
                ChromaticPolynomCreator.PolyToken('O_{1}'),
                ChromaticPolynomCreator.PolyToken('O_{1}', False),
            ],
            '(0) * O_{1}',
        ),
        (
            [
                ChromaticPolynomCreator.PolyToken('O_{1}'),
                ChromaticPolynomCreator.PolyToken('O_{1}'),
            ],
            '(2) * O_{1}',
        ),
        (
            [
                ChromaticPolynomCreator.PolyToken('O_{1}'),
                ChromaticPolynomCreator.PolyToken('O_{1}'),
                ChromaticPolynomCreator.PolyToken('O_{2}'),
                ChromaticPolynomCreator.PolyToken('O_{2}'),
                ChromaticPolynomCreator.PolyToken('O_{3}', False),
                ChromaticPolynomCreator.PolyToken('O_{4}'),
                ChromaticPolynomCreator.PolyToken('O_{5}', False),
            ],
            '(2) * O_{1} + (2) * O_{2} + O_{4} + -O_{3} + -O_{5}',
        ),
    ),
)
def test_simplify_polynom(raw_polynom, expected):
    simplified = ChromaticPolynomCreator.simplify_polynom(raw_polynom)
    assert simplified == expected
