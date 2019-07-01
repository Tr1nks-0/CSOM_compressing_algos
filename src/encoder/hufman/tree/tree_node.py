# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N1

# нода дерева Хаффмана
class Node:

    def __init__(self, character: int = None, frequency: int = 0,
                 left_child: 'Node' = None, right_child: 'Node' = None) -> 'Node':
        if frequency > 0:
            self.frequency: int = frequency
        if character is not None:
            if left_child is not None or right_child is not None:
                raise RuntimeError('Attempt to add data to connection node')
            self.character: int = character
            self.left_child = None
            self.right_child = None
        else:
            self.left_child: 'Node' = left_child
            self.right_child: 'Node' = right_child

    @classmethod
    def data_node(cls, character: int, frequency: int = 0) -> 'Node':
        return cls(character=character, frequency=frequency)

    @classmethod
    def connection_node(cls, left_child: 'Node' = None, right_child: 'Node' = None, frequency: int = 0) -> 'Node':
        return cls(left_child=left_child, right_child=right_child, frequency=frequency)

    def is_data(self) -> bool:
        return hasattr(self, 'character') and self.character is not None

    def has_left_child(self) -> bool:
        return hasattr(self, 'left_child') and self.left_child is not None

    def has_right_child(self) -> bool:
        return hasattr(self, 'right_child') and self.right_child is not None

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if self.is_data():
            return other.is_data() and self.character == other.character
        else:
            return not other.is_data() and self.left_child == other.left_child and self.right_child == other.right_child

    def __lt__(self, other: 'Node'):
        return self.frequency < other.frequency

    def __le__(self, other: 'Node'):
        return self.frequency <= other.frequency

    def __gt__(self, other: 'Node'):
        return self.frequency > other.frequency

    def __ge__(self, other: 'Node'):
        return self.frequency >= other.frequency
