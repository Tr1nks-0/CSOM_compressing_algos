from io import BytesIO
from unittest import TestCase

from src.hufman.dto.tree_node import TreeNode
from src.hufman.hufman_tree_encoder import write_tree_to_file, read_tree_from_file


class HufmanTreeEncoderTest(TestCase):
    def setUp(self) -> None:
        # self.tree = TreeNode(
        #     left_child=TreeNode(
        #         left_child=TreeNode(character=255),
        #         right_child=TreeNode(character=254)
        #     ),
        #     right_child=TreeNode(
        #         left_child=TreeNode(
        #             left_child=TreeNode(character=253),
        #             right_child=TreeNode(character=252)
        #         )
        #     )
        # )
        self.tree = TreeNode(
            left_child=TreeNode(
                left_child=TreeNode(character=2),
                right_child=TreeNode(character=5)
            ),
            right_child=TreeNode(
                left_child=TreeNode(left_child=TreeNode(character=1),
                                    right_child=TreeNode(left_child=TreeNode(character=4),
                                                         right_child=TreeNode(character=7)
                                                         )
                                    ),
                right_child=TreeNode(character=3)
            )

        )

    def test_should_encode_and_read_tree_without_loosing_data(self):
        virtual_file = BytesIO()
        write_tree_to_file(self.tree, virtual_file)
        virtual_file.seek(0)
        readed = read_tree_from_file(virtual_file)
        self.assertEqual(self.tree, readed)
