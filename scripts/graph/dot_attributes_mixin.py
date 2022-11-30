from abc import ABC, abstractmethod
from typing import Dict


class DotAttributesMixin(ABC):

    _dot_attributes = {}

    def set_dot_attributes(self, dot_data: Dict[str, str] = None):
        self._dot_attributes = dot_data

    def update_dot_attributes(self, dot_data: Dict[str, str]):
        self._dot_attributes.update(dot_data)
    
    def _get_attributes_string(self):
        if not self._dot_attributes:
            return ''
        attributes = ','.join(f'{k}={v}' for k, v in self._dot_attributes.items())
        return f'[{attributes}]'
