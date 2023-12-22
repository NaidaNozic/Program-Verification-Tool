from program.statement import Statement


class Unlock(Statement):
    lock_id: str
    __match_args__ = ('line', 'column', 'lock_id')

    def __init__(self, line: int, column: int, lock_id: str) -> None:
        super().__init__(line, column)
        self.lock_id = lock_id

    def __str__(self):
        return 'Unlock({lock_id})'.format(lock_id=self.lock_id)
