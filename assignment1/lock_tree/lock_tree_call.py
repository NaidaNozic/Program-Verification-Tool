from program.statement import Statement
from enum import Enum


class LockTreeCallType(Enum):
    LOCK = 1
    UNLOCK = 2


class LockTreeCall(Statement):
    lock_id: str
    type: LockTreeCallType
    __match_args__ = ('line', 'column', 'lock_id', 'type')

    def __init__(self, line: int, column: int, lock_id: str, type: LockTreeCallType) -> None:
        super().__init__(line, column)
        self.lock_id = lock_id
        self.type = type

    def __str__(self):
        return 'LockTreeCall({lock_id}, {type})'.format(lock_id=self.lock_id, type=self.type.name)
