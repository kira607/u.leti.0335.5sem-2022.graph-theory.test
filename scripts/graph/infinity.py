from typing import Union


class Infinity:

    def __gt__(self, _: int):
        return True

    def __ge__(self, _: int):
        return True

    def __lt__(self, _: int):
        return False

    def __le__(self, _: int):
        return False

    def __eq__(self, _: int):
        return isinstance(_, Infinity)

    def __add__(self, _: int):
        return self

    def __radd__(self, _: int):
        return self

    def __repr__(self):
        return 'oo'


inf = Infinity()
InfInt = Union[Infinity, int]
InfNum = Union[InfInt, float]
