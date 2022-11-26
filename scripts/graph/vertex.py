from dataclasses import dataclass, field
from typing import Optional

from .dot_attributes_mixin import DotAttributesMixin


@dataclass
class Vertex(DotAttributesMixin):
    name: str = field(hash=True)
    number: Optional[int] = None
    eccentricity: Optional[int] = None

    def __hash__(self):
        return hash(self.name)

    def _get_dot_string(self) -> str:
        return f'"{self.name}"'