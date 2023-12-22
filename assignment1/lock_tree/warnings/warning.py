Lock = tuple[str, int, int]
LockPattern = tuple[Lock, Lock]
ThreadLockPattern = tuple[str, LockPattern]

class Warning:
    message: str

    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message
