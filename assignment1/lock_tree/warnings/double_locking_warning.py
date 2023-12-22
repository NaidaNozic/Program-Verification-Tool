from assignment1.lock_tree.warnings.warning import Warning, LockPattern
from os import linesep


class DoubleLockingWarning(Warning):
    thread_id: str
    lock_pattern: LockPattern

    def __init__(self, thread_id: str, lock_pattern: LockPattern) -> None:
        super().__init__('Double locking detected:' + linesep + '{thread_id} locking of {lock_1_id} on ({lock_1_line},{lock_1_column}) and ({lock_2_line},{lock_2_column})'.format(
            thread_id=thread_id,
            lock_1_id=lock_pattern[0][0],
            lock_1_line=lock_pattern[0][1],
            lock_1_column=lock_pattern[0][2],
            lock_2_line=lock_pattern[1][1],
            lock_2_column=lock_pattern[1][2]
        ))
        self.thread_id = thread_id
        self.lock_pattern = lock_pattern