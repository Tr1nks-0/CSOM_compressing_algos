from unittest import TestCase

from hufman.tree.tree_node import Node


class TreeNodeTests(TestCase):

    def test_throw_runtime_error_when_add_char_to_connection_node(self):
        self.assertRaises(RuntimeError, Node, character=b'\xff', frequency=10, left_child=object(), right_child=None)

    def test_sort_asc_by_frequencies(self):
        unsorted = [
            Node.data_node(b'\xff', 3),
            Node.data_node(b'\xff', 1),
            Node.data_node(b'\xff', 5),
            Node.data_node(b'\xff', 4),
            Node.data_node(b'\xff', 2),
        ]
        sorted = unsorted.copy()
        sorted.sort()
        for i in range(len(sorted)):
            self.assertEqual(i + 1, sorted[i].frequency)
