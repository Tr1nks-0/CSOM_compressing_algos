from io import BytesIO
from unittest import TestCase

from src.hufman.dto.tree_node import TreeNode
from src.hufman.hufman_tree_encoder import write_tree_to_file, read_tree_from_file


class HufmanTreeEncoderTest(TestCase):
    def setUp(self) -> None:
        self.tree = TreeNode(  # A
            left_child=TreeNode(  # B
                left_child=TreeNode(character=2),  # C
                right_child=TreeNode(character=5)  # D
            ),
            right_child=TreeNode(  # E
                left_child=TreeNode(  # F
                    left_child=TreeNode(character=1),  # G
                    right_child=TreeNode(  # H
                        left_child=TreeNode(character=4),  # I
                        right_child=TreeNode(character=7)  # J
                    )
                ),
                right_child=TreeNode(character=3)  # K
            )
        )

    def test_should_encode_and_read_tree_without_loosing_data(self):
        virtual_file = BytesIO()
        write_tree_to_file(self.tree, virtual_file)
        # with open('C:/W/controlsSystemOptimisationMethods/resources/oooo', 'wb') as file:
        #     write_tree_to_file(self.tree, file)
        virtual_file.seek(0)
        readed = read_tree_from_file(virtual_file)
        self.assertEqual(self.tree, readed)
#
