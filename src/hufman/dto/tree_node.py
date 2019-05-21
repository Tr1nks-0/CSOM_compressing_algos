from typing import List


class TreeNode:
    def __init__(self, character=None, frequency=0, left_child=None, right_child=None, parent=None):
        self.character: int = character
        self.frequency = frequency
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent

    def fill_code_table(self, table: dict, key: int = 0) -> dict:
        if not self.left_child and not self.right_child:
            table[self.character] = key
        else:
            self.left_child.fill_code_table(table, key << 1)
            self.right_child.fill_code_table(table, key << 1 | 1)
        return table

    def tree_to_list(self, list: List['TreeNode'] = None) -> list:
        if list is None:
            list = []
        list.append(self)
        if self.left_child:
            self.left_child.tree_to_list(list)
        if self.right_child:
            self.right_child.tree_to_list(list)
        return list

    def __lt__(self, other: 'TreeNode'):
        return self.frequency < other.frequency

    def __le__(self, other: 'TreeNode'):
        return self.frequency <= other.frequency

    def __eq__(self, other: 'TreeNode'):
        if not other:
            return False
        if self.character:
            return self.character == other.character if other.character else False
        else:
            return self.frequency == other.frequency and \
                   self.left_child == other.left_child and \
                   self.right_child == other.right_child

    def __gt__(self, other: 'TreeNode'):
        return self.frequency > other.frequency

    def __ge__(self, other: 'TreeNode'):
        return self.frequency >= other.frequency
