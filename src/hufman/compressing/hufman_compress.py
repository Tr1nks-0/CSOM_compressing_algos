import math
from typing import BinaryIO

from hufman.tree.tree_node import Node
from hufman.tree.tree_utils import build_tree_from_bytes, tree_to_codetable, tree_to_bytes, tree_from_io


def compress_to_file(data: bytes, filename: str) -> None:
    with open(filename, 'wb') as file:
        compress_to_io(data, file)


def compress_to_io(data: bytes, io: BinaryIO) -> None:
    io.write(compress_to_bytes(data))


def compress_to_bytes(data: bytes) -> bytes:
    hufman_tree = build_tree_from_bytes(data)
    code_table = tree_to_codetable(hufman_tree)
    temp = 0
    for byte in data:
        encoded = code_table.get(byte)
        temp = temp << len(encoded) | int(encoded, 2)
    bit_str = bin(temp)[2:]
    bit_count = len(bit_str)
    reduced_bit_count = math.ceil(bit_count / 8) * 8
    bit_str = bit_str + '0' * (reduced_bit_count - bit_count)

    return tree_to_bytes(hufman_tree) + bytes(int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))


def restore_from_file(filename: str) -> bytes:
    with open(filename, 'rb') as file:
        return restore_from_io(file)


def restore_from_io(io: BinaryIO) -> bytes:
    hufman_tree, nodes_count = tree_from_io(io)
    data = io.read()

    reduced_bit_count = len(data) * 8
    bit_count = nodes_count * 19
    data_int = int.from_bytes(data, 'big')
    data_bits = bin(data_int)[2:].zfill(reduced_bit_count)
    restored_data = bytearray()
    node = hufman_tree
    print(data_bits)
    for bit_str in data_bits:
        if bit_str == '1':
            node = node.right_child
            print('r ', end='')
        else:
            node = node.left_child
            print('l ', end='')
        if node.is_data():
            print(f'   {node.character}')
            restored_data.append(node.character)
            node = hufman_tree
    return restored_data
