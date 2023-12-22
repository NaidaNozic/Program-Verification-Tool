from assignment1.lock_tree.warnings.warning import Warning, LockPattern
from os import linesep


class InvalidLockingPatternWarning(Warning):
    thread_id: str
    lock_pattern: LockPattern

    def __init__(self, thread_id: str, lock_pattern: LockPattern) -> None:
        super().__init__('Invalid locking pattern detected:' + linesep + '{thread_id} unlocked {lock_unlocked_id}({lock_unlocked_line},{lock_unlocked_column}) istead of {lock_id}({lock_line},{lock_column})'.format(
            thread_id=thread_id,
            lock_unlocked_id=lock_pattern[0][0],
            lock_unlocked_line=lock_pattern[0][1],
            lock_unlocked_column=lock_pattern[0][2],
            lock_id=lock_pattern[1][0],
            lock_line=lock_pattern[1][1],
            lock_column=lock_pattern[1][2]
        ))
        self.thread_id = thread_id
        self.lock_pattern = lock_pattern
