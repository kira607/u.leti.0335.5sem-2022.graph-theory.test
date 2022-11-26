from dataclasses import dataclass, field
from typing import Optional, Dict

from .vertex import Vertex
from .dot_attributes_mixin import DotAttributesMixin


@dataclass
class Edge(DotAttributesMixin):
    v1: Vertex
    v2: Vertex
    directional: bool = False
    weight: Optional[float] = None

    @property
    def dot(self):
        arrow = '->' if self.directional else '--'
        attributes = self._get_attributes_string()
        dot = f'{self.v1.name} {arrow} {self.v2.name} {attributes}'
        return dot
