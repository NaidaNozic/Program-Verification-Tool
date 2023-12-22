from typing_extensions import Self


class Node:
    thread_id: str
    lock_id: str | None
    line: int
    column: int
    parent: Self | None
    children: list[Self]

    def __init__(self, thread_id: str, lock_id: str | None, line: int, column: int, children: list[Self]) -> None:
        self.thread_id = thread_id
        self.lock_id = lock_id
        self.line = line
        self.column = column
        self.parent = None
        self.children = children

    def add_child(self, node: Self):
        node.parent = self
        self.children.append(node)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Node) and __value.lock_id == self.lock_id
    
    def __hash__(self) -> int:
        return self.lock_id.__hash__()
    
    #HELP FUNCTIONS
    def __str__(self) -> str:
        return "("+self.lock_id+","+str(self.line)+","+str(self.column)+")"
