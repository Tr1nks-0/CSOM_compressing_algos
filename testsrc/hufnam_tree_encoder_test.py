from unittest import TestCase

from src.hufman.dto.tree_node import TreeNode


class HufmanTreeEncoderTest(TestCase):
    def setUp(self) -> None:
        self.tree = TreeNode(
            left_child=TreeNode(
                left_child=TreeNode(character=65535),
                right_child=TreeNode(character=65534)
            ),
            right_child=TreeNode(
                left_child=TreeNode(
                    left_child=TreeNode(character=65533),
                    right_child=TreeNode(character=65532)
                )
            )
        )
