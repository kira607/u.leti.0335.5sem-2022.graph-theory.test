class _Missing:
    def __copy__(self):
        return self

    def __deepcopy__(self):
        return self

    def __repr__(self):
        return f'<{str(self)}>'

    def __str__(self):
        return f'{self.__class__.__name__}'


MISSING = _Missing()
