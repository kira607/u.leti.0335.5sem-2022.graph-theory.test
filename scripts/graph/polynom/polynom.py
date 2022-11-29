import re
from dataclasses import dataclass, field
from typing import Any, Optional, TypeVar


@dataclass
class Var:
    name: str = field(hash=True)


class PolyToken:
    def __init__(self, var: Optional[str | Var] = None, multiplier: float = 1.0, power: float = 1.0):

        if isinstance(var, Var):
            self.var = var
        elif isinstance(var, str):
            self.var = Var(var)
        else:
            self.var = None

        self.multiplier = multiplier
        self.power = power

    def swap_sign(self):
        self.multiplier = -self.multiplier
        return self

    def __str__(self):
        multiplier = self.multiplier

        if multiplier == 1:
            multiplier = ''
        # elif multiplier == -1:
        #     multiplier_string = '-'
        else:
            multiplier = f'({multiplier})'

        var = '' if self.var is None else self.var.name
        times = ' * ' if multiplier else ''
        power = self.power if self.power != 1 else ''
        to = '^{' if power else ''
        end = '}' if power else ''

        return f'{multiplier}{times}{var}{to}{power}{end}'

    def __mul__(self, other: float):
        self.multiplier *= other

    def __repr__(self):
        return f'<{self.__class__.__name__} {str(self)}>'

    def __hash__(self):
        return hash(repr(self))


_TPolynom = TypeVar(name='_TPolynom', bound='Polynom')
_OtherPolynom = str | int | float | Var | PolyToken | _TPolynom


class Polynom:
    def __init__(self) -> None:
        self._tokens = []

    @classmethod
    def from_tokens(cls, *tokens: _OtherPolynom) -> _TPolynom:
        obj = cls()
        for t in tokens:
            obj += t
        return obj

    def swap_sign(self):
        for token in self._tokens:
            token.swap_sign()
        return self

    def __str__(self) -> str:
        self._tokens = sorted(self._tokens, key=lambda t: t.power, reverse=True)
        string = ' + '.join(str(token) for token in self._tokens)
        return string

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} {str(self)}>'

    def __neg__(self) -> _TPolynom:
        p = Polynom()
        for token in self._tokens:
            p += token.swap_sign()
        return p

    def __pos__(self) -> _TPolynom:
        return self

    def __add__(self, other: _OtherPolynom) -> _TPolynom:
        other = self._resolve_other('__add__', other)

        if isinstance(other, PolyToken):
            self._add_token(other)
        elif isinstance(other, Polynom):
            for t in other._tokens:
                self._add_token(t)

        return self

    def __radd__(self, other: _OtherPolynom) -> _TPolynom:
        return self + other

    def __iadd__(self, other: _OtherPolynom) -> _TPolynom:
        return self + other

    def __sub__(self, other: _OtherPolynom) -> _TPolynom:
        other = self._resolve_other('__sub__', other)
        return self + other.swap_sign()

    def __rsub__(self, other: _OtherPolynom) -> _TPolynom:
        return self - other

    def __isub__(self, other: _OtherPolynom) -> _TPolynom:
        return self - other

    def _add_token(self, t: PolyToken) -> None:
        for t1 in self._tokens:
            if t1.power == t.power and t1.var == t.var:
                t1.multiplier += t.multiplier
                return
        self._tokens.append(t)

    def _resolve_other(self, method_name: str, other: _OtherPolynom) -> PolyToken | _TPolynom:
        if isinstance(other, str):
            try:
                other = float(other)
            except ValueError:
                self._raise_not_supported_type(method_name, other)

        if isinstance(other, int) or isinstance(other, float):
            other = PolyToken(multiplier=float(other))

        if isinstance(other, Var):
            other = PolyToken(other)

        self._type_check(method_name, other)

        return other

    def _type_check(self, method_name: str, other: _OtherPolynom) -> None:
        if isinstance(other, PolyToken) or isinstance(other, Polynom):
            return
        self._raise_not_supported_type(method_name, other)

    def _raise_not_supported_type(self, method_name: str, other: Any) -> None:
        raise TypeError(f'{method_name} is not supported between {self.__class__.__name__} and {type(other).__name__}')
