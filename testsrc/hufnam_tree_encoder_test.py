from io import BytesIO
from unittest import TestCase

from src.hufman.dto.tree_node import TreeNode
from src.hufman.hufman_tree_encoder import tree_to_io, tree_from_io


class HufmanTreeEncoderTest(TestCase):
    def setUp(self) -> None:
        self.tree = TreeNode(
            left_child=TreeNode(
                left_child=TreeNode(character=255),
                right_child=TreeNode(character=254)
            ),
            right_child=TreeNode(
                left_child=TreeNode(
                    left_child=TreeNode(character=253),
                    right_child=TreeNode(character=252)
                )
            )
        )

    def test_should_encode_and_read_tree_without_loosing_data(self):
        virtual_file = BytesIO()
        tree_to_io(self.tree, virtual_file)
        virtual_file.seek(0)
        readed = tree_from_io(virtual_file)
        self.assertEqual(self.tree, readed)
