class Node:
    def __init__(self, character=None, frequency=0, left_child=None, right_child=None) -> 'Node':
        if frequency > 0:
            self.frequency = frequency
        if character is not None:
            if left_child is not None or right_child is not None:
                raise RuntimeError('Attempt to add data to connection node')
            self.character = character
        else:
            if left_child is not None:
                self.left_child = left_child
            if right_child is not None:
                self.right_child = right_child

    @classmethod
    def data_node(cls, character, frequency=0) -> 'Node':
        return cls(character=character, frequency=frequency)

    @classmethod
    def connection_node(cls, left_child=None, right_child=None, frequency=0) -> 'Node':
        return cls(left_child=left_child, right_child=right_child, frequency=frequency)

    def is_data(self) -> bool:
        return self.character is not None

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if self.is_data():
            return other.is_data() and self.character == other.character
        else:
            return not other.is_data() and \
                   self.left_child == other.left_child and \
                   self.right_child == other.right_child

    def __lt__(self, other: 'Node'):
        return self.frequency < other.frequency

    def __le__(self, other: 'Node'):
        return self.frequency <= other.frequency

    def __gt__(self, other: 'Node'):
        return self.frequency > other.frequency

    def __ge__(self, other: 'Node'):
        return self.frequency >= other.frequency
