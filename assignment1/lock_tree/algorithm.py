from assignment1.lock_tree.lock_tree_call import LockTreeCall
from assignment1.lock_tree.node import Node
from assignment1.lock_tree.warnings.warning import Warning
from assignment1.lock_tree.lock_tree_call import LockTreeCallType
from assignment1.lock_tree.warnings.double_locking_warning import DoubleLockingWarning
from assignment1.lock_tree.warnings.invalid_locking_pattern_warning import InvalidLockingPatternWarning
from assignment1.lock_tree.warnings.invalid_unlocking_warning import InvalidUnlockingWarning
from assignment1.lock_tree.warnings.deadlock_warning import DeadlockWarning


def build_lock_tree(locks_tree_calls: tuple[str, list[LockTreeCall]], warnings: list[Warning]) -> Node | None:

    if not locks_tree_calls:
        return None
    
    locked = {} # lock_id : call
    unlocked = {} # lock_id : call

    root = Node(thread_id=locks_tree_calls[0], lock_id="root", line=0, column=0, children=[])
    current_node = root

    for call in locks_tree_calls[1]:
        if call.type == LockTreeCallType.LOCK:
            if call.lock_id not in locked:
                lock_node = Node(thread_id=locks_tree_calls[0], lock_id=call.lock_id, line=call.line, column=call.column, children=[])
                current_node.add_child(lock_node)
                current_node = lock_node
                locked[call.lock_id] = call
            else:
                lock_pattern = ((call.lock_id, call.line, call.column),
                                (call.lock_id, locked[call.lock_id].line, locked[call.lock_id].column))
                double_lock_warning = DoubleLockingWarning(thread_id=root.thread_id, lock_pattern=lock_pattern)
                warnings.append(double_lock_warning)
                return root

        elif call.type == LockTreeCallType.UNLOCK:
            
            if call.lock_id not in locked:
                lock = (call.lock_id, call.line, call.column)
                invalid_unlocking_warning = InvalidUnlockingWarning(thread_id=root.thread_id, lock = lock)
                warnings.append(invalid_unlocking_warning)
                return root
            
            if call.lock_id != current_node.lock_id:
                lock_pattern = ((call.lock_id, call.line, call.column),
                                (current_node.lock_id, current_node.line, current_node.column))
                invalid_locking_warning = InvalidLockingPatternWarning(thread_id=root.thread_id, lock_pattern=lock_pattern)
                warnings.append(invalid_locking_warning)
                return root
            
            if current_node.parent:
                locked.pop(current_node.lock_id)
                unlocked[current_node.lock_id] = call
                current_node = current_node.parent

    return root

def check(threads_lock_tree_calls: tuple[tuple[str, list[LockTreeCall]], tuple[str, list[LockTreeCall]]],
          warnings: list[Warning]):
    warnings1 = []
    warnings2 = []
    root1 = build_lock_tree(threads_lock_tree_calls[0], warnings1)
    root2 = build_lock_tree(threads_lock_tree_calls[1], warnings2)
    if root1.children and root2.children:
        for node1 in root1.children:
            branches1 = get_branches(node1)
            for node2 in root2.children:
                branches2 = get_branches(node2)
                
                common_locks = []

                for branch1 in branches1:
                    for branch2 in branches2:
                        common_locks = find_common_locks(branch1, branch2)
                        if len(common_locks) == 2:
                            if is_valid_deadlock(branch1, branch2, common_locks):
                                deadlock_information = create_deadlock_information(root1, branch1, branch2, common_locks, root2)
                                deadlock_warning = DeadlockWarning(deadlock_information)
                                if deadlock_warning not in warnings:
                                    warnings.append(deadlock_warning)

    warnings.sort(key=custom_sort)
    warnings = warnings1 + warnings2 + warnings

def custom_sort(item):
    return (item.deadlock_information[0][1][0][1], item.deadlock_information[0][1][1][1])

def find_common_locks(branch1 : list[Node],branch2 : list[Node]) -> list[Node]:
    common_locks = [node1 for node1 in branch1 if node1 in branch2][:2]
    return common_locks

def is_valid_deadlock(branch1, branch2, common_locks):

    set1 = set(branch1[:branch1.index(common_locks[1])])
    set2 = set(branch2[:max(branch2.index(common_locks[0]), branch2.index(common_locks[1]))])

    return (
        len(set1.intersection(set2).difference(set(common_locks))) == 0
        and branch1.index(common_locks[0]) < branch1.index(common_locks[1])
        and branch2.index(common_locks[1]) < branch2.index(common_locks[0])
    )

def create_deadlock_information(root1, branch1, branch2, common_locks, root2):
    lock_pattern1 = (
        (branch1[branch1.index(common_locks[0])].lock_id, branch1[branch1.index(common_locks[0])].line, branch1[branch1.index(common_locks[0])].column),
        (branch1[branch1.index(common_locks[1])].lock_id, branch1[branch1.index(common_locks[1])].line, branch1[branch1.index(common_locks[1])].column)
    )
    lock_pattern2 = (
        (branch2[branch2.index(common_locks[1])].lock_id, branch2[branch2.index(common_locks[1])].line, branch2[branch2.index(common_locks[1])].column),
        (branch2[branch2.index(common_locks[0])].lock_id, branch2[branch2.index(common_locks[0])].line, branch2[branch2.index(common_locks[0])].column)
    )
    return (
        (root1.thread_id, lock_pattern1),
        (root2.thread_id, lock_pattern2)
    )

def get_branches(root: Node)-> list[list[Node]] | None:
    branches=[]

    def dfs(node: Node, current_branch: list[Node]):
        if node is None:
            return
        
        current_branch.append(node)

        if len(node.children) == 0:
            branches.append(current_branch.copy())
        else:
            for child in node.children:
                dfs(child, current_branch)

        current_branch.pop()

    dfs(root, [])
    return branches