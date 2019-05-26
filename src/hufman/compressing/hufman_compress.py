import math
from typing import BinaryIO

from hufman.tree.tree_node import Node
from hufman.tree.tree_utils import build_tree_from_bytes, tree_to_codetable, tree_to_bytes, tree_from_io


def compress_to_file(data: bytes, filename: str) -> None:
    with open(filename, 'wb') as file:
        compress_to_io(data, file)


def restore_from_file(filename: str) -> bytes:
    with open(filename, 'rb') as file:
        return restore_from_io(file)


def compress_to_io(data: bytes, io: BinaryIO) -> None:
    io.write(compress_to_bytes(data))


def compress_to_bytes(data: bytes) -> bytes:
    hufman_tree = build_tree_from_bytes(data)
    code_table = tree_to_codetable(hufman_tree)
    temp = 0
    leading_zero_count = 0
    first_1_reached = False
    for byte in data:
        encoded = code_table.get(byte)

        if not first_1_reached:
            if '1' in encoded:
                first_1_reached = True
                leading_zero_count += encoded.index('1')
            else:
                leading_zero_count += len(encoded)

        temp = temp << len(encoded) | int(encoded, 2)
    bit_str = '0' * leading_zero_count + bin(temp)[2:]
    bit_count = len(bit_str)
    reduced_bit_count = math.ceil(bit_count / 8) * 8
    bit_str = bit_str + '0' * (reduced_bit_count - bit_count)
    print(bit_str)
    # debug(hufman_tree, code_table, data)
    return tree_to_bytes(hufman_tree) + bytes(int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))


def debug(tree, codetable, data):
    # r l r l l r l r    175
    a = tree.right_child.left_child.right_child.left_child.left_child.right_child.left_child.right_child.character
    print(a)
    b = data[0]
    print(b)
    c = codetable.get(b)
    print(c)
    print()


def restore_from_io(io: BinaryIO) -> bytes:
    hufman_tree, nodes_count = tree_from_io(io)
    data = io.read()

    reduced_bit_count = len(data) * 8
    data_int = int.from_bytes(data, 'big')
    data_bits = bin(data_int)[2:].zfill(reduced_bit_count)
    restored_data = bytearray()
    node = hufman_tree
    print(data_bits)
    for bit_str in data_bits:
        if bit_str == '1':
            node = node.right_child
        else:
            node = node.left_child
        if node.is_data():
            restored_data.append(node.character)
            node = hufman_tree
    return restored_data
