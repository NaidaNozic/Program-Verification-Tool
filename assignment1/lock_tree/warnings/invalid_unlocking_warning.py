from assignment1.lock_tree.warnings.warning import Warning, Lock
from os import linesep


class InvalidUnlockingWarning(Warning):
    thread_id: str
    lock: Lock

    def __init__(self, thread_id: str, lock: Lock) -> None:
        super().__init__('Invalid unlocking detected:' + linesep + '{thread_id} invalid unlocking of {lock_id}({line},{column})'.format(
            thread_id=thread_id,
            lock_id=lock[0],
            line=lock[1],
            column=lock[2]
        ))
        self.thread_id = thread_id
        self.lock = lock