from .dot_attributes_mixin import DotAttributesMixin


class Vertex(DotAttributesMixin):
    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} \'{self.name}\'>'

    def __str__(self) -> str:
        return repr(self)

    def __eq__(self, other: 'Vertex') -> bool:
        return hash(self) == hash(other)

    def __hash__(self) -> int:
        return hash(self.name)

    def _get_dot_string(self) -> str:
        return f'"{self.name}"'
