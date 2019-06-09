import math
import os
from typing import BinaryIO, Tuple

from encoder.encoder import Encoder
from encoder.hufman.tree.tree_node import Node
from encoder.hufman.tree.tree_utils import build_tree_from_bytes, tree_to_codetable, tree_to_bytes, tree_from_io


# NAME: Sergey Baydin, 8.04.122.010.18.2
# ASGN: N1

class HufmanEncoder(Encoder):
    def __init__(self):
        super().__init__()
        self.default_extension = 'hfm'
        self.name = 'Hufman'

    def compress_to_io(self, data: bytes, io: BinaryIO) -> tuple:
        data, meta = self.compress_to_bytes(data)
        io.write(data)
        return meta

    def restore_from_io(self, io: BinaryIO) -> bytes:
        hufman_tree, nodes_count = tree_from_io(io)
        if nodes_count == 0:
            return bytes()
        data = io.read()
        return self.restore_from_bytes(hufman_tree, data)

    def compress_to_bytes(self, data: bytes) -> Tuple[bytes, tuple]:
        if len(data) == 0:
            return data, (0, 0)
        hufman_tree = build_tree_from_bytes(data)
        code_table = tree_to_codetable(hufman_tree)
        bit_str = '000'
        for byte in data:
            encoded = code_table.get(byte)
            bit_str = bit_str + encoded
        bit_count = len(bit_str)
        reduced_bit_count = math.ceil(bit_count / 8) * 8
        byte_complete_offset = reduced_bit_count - bit_count
        bit_str = bin(byte_complete_offset)[2:].zfill(3) + bit_str[3:] + '0' * byte_complete_offset
        compressed = tree_to_bytes(hufman_tree) + bytes(
            int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))
        return compressed, self.calculate_meta(len(data), len(compressed))

    def restore_from_bytes(self, hufman_tree: Node, data: bytes) -> bytes:
        if len(data) == 0:
            return data
        reduced_bit_count = len(data) * 8
        data_int = int.from_bytes(data, 'big')
        data_bits = bin(data_int)[2:].zfill(reduced_bit_count)
        byte_complete_offset = int(data_bits[:3], 2)
        data_bits = data_bits[3:len(data_bits) - byte_complete_offset]
        restored_data = bytearray()
        node = hufman_tree
        for bit_str in data_bits:
            if bit_str == '1' and node.right_child:
                node = node.right_child
            elif node.left_child:
                node = node.left_child
            if node.is_data():
                restored_data.append(node.character)
                node = hufman_tree
        return restored_data
