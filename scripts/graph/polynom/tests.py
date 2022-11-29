from contextlib import nullcontext

import pytest

from .polynom import Var, Polynom, PolyToken


NO_ERROR = nullcontext()


@pytest.mark.parametrize(
    'args, expectation',
    (
        (['1'], NO_ERROR),
        ([1], NO_ERROR),
        ([1.234], NO_ERROR),
        ([PolyToken()], NO_ERROR),
        ([Polynom()], NO_ERROR),
        ([['1']], pytest.raises(TypeError)),
        ([{}], pytest.raises(TypeError)),
        ([(1, 2)], pytest.raises(TypeError)),
    ),
)
def test_init(args, expectation) -> None:
    with expectation:
        Polynom(*args)


@pytest.mark.parametrize(
    'polynom, expected_result',
    (
        (Polynom.from_tokens('1'), '(-1.0)'),
        (Polynom.from_tokens(Var('x')), '(-1.0) * x'),
    ),
)
def test_neg(polynom, expected_result) -> None:
    p = -polynom
    assert str(p) == expected_result


@pytest.mark.parametrize(
    'p1, p2, expected_result',
    (
        (
            Polynom.from_tokens(Var('x'), 99),
            Polynom.from_tokens(Var('x'), 101),
            '(2.0) * x + (200.0)'
        ),
    ),
)
def test_add(p1, p2, expected_result):
    p = p1 + p2
    assert str(p) == expected_result


@pytest.mark.parametrize(
    'p1, p2, expected_result',
    (
        (
            Polynom.from_tokens(Var('x'), 99),
            Polynom.from_tokens(Var('x'), 101),
            '(0.0) * x + (-2.0)'
        ),
    ),
)
def test_sub(p1, p2, expected_result):
    p = p1 - p2
    assert str(p) == expected_result
