class BaseTask:

    def __init__(self, number: int) -> None:
        self.number = number
    
    def solve(self) -> None:
        print(f'#### TASK №{self.number} SOLUTION ####')
        self._solve()

    def _solve(self) -> None:
        raise NotImplementedError()
