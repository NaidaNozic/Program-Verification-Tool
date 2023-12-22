from assignment1.lock_tree.warnings.warning import Warning, ThreadLockPattern
from os import linesep


class DeadlockWarning(Warning):
    deadlock_information: tuple[ThreadLockPattern, ThreadLockPattern]

    def __init__(self, deadlock_information: tuple[ThreadLockPattern, ThreadLockPattern]) -> None:
        super().__init__('Potential deadlock situation detected:' + linesep + linesep.join([
            '{thread_id} locked {locking_pattern}'.format(
                thread_id=thread_lock_pattern[0],
                locking_pattern=' and '.join(['{lock_id}({line},{column})'.format(
                    lock_id=locking_pattern[0], 
                    line=locking_pattern[1], 
                    column=locking_pattern[2]
                ) for locking_pattern in thread_lock_pattern[1]])
            ) for thread_lock_pattern in deadlock_information
        ]))
        self.deadlock_information = deadlock_information

    def __eq__(self, other):
        return isinstance(other, DeadlockWarning) and str(self) == str(other)
