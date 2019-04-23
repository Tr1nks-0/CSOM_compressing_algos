class TreeNode:
    def __init__(self, character=None, frequency=0, left_child=None, right_child=None, parent=None):
        self.character = character
        self.frequency = frequency
        self.left_child = left_child
        self.right_child = right_child
        self.parent = parent

    def fill_code_table(self, table: dict, key: int = 0) -> None:
        if not self.left_child and not self.right_child:
            table[self.character] = key
        else:
            self.left_child.fill_code_table(table, key << 1)
            self.right_child.fill_code_table(table, key << 1 | 1)

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __le__(self, other):
        return self.frequency <= other.frequency

    def __eq__(self, other):
        return self.frequency == other.frequency

    def __gt__(self, other):
        return self.frequency > other.frequency

    def __ge__(self, other):
        return self.frequency >= other.frequency
