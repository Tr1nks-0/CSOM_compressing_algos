import json

import math
import os
from typing import BinaryIO, Tuple

from hufman.tree.tree_json_encoder import TreeEncoder
from hufman.tree.tree_node import Node
from hufman.tree.tree_utils import build_tree_from_bytes, tree_to_codetable, tree_to_bytes, tree_from_io


def compress_file(filename: str) -> tuple:
    with open(filename, 'rb') as input_file:
        data = input_file.read()
        return compress_to_file(data, str(filename) + '.hfm')


def restore_file(filename: str) -> str:
    restored = restore_from_file(filename)
    restored_filename = __resolve_restored_filename(filename)
    with open(restored_filename, 'wb') as file:
        file.write(restored)
    return restored_filename


def compress_to_file(data: bytes, filename: str) -> tuple:
    with open(filename, 'wb') as file:
        return compress_to_io(data, file)


def restore_from_file(filename: str) -> bytes:
    with open(filename, 'rb') as file:
        return restore_from_io(file)


def compress_to_io(data: bytes, io: BinaryIO) -> tuple:
    data, meta = compress_to_bytes(data)
    io.write(data)
    return meta


def restore_from_io(io: BinaryIO) -> bytes:
    hufman_tree, nodes_count = tree_from_io(io)
    data = io.read()
    return restore_from_bytes(hufman_tree, data)


def compress_to_bytes(data: bytes) -> Tuple[bytes, tuple]:
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
    compressed = tree_to_bytes(hufman_tree) + bytes(int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))
    return compressed, calculate_meta(len(data), len(compressed))


def restore_from_bytes(hufman_tree: Node, data: bytes) -> bytes:
    reduced_bit_count = len(data) * 8
    data_int = int.from_bytes(data, 'big')
    data_bits = bin(data_int)[2:].zfill(reduced_bit_count)
    byte_complete_offset = int(data_bits[:3], 2)
    data_bits = data_bits[3:len(data_bits) - byte_complete_offset]
    restored_data = bytearray()
    node = hufman_tree
    for bit_str in data_bits:
        if bit_str == '1':
            node = node.right_child
        else:
            node = node.left_child
        if node.is_data():
            restored_data.append(node.character)
            node = hufman_tree
    return restored_data


def calculate_meta(initial_length, compressed_length):
    size_different = initial_length - compressed_length
    rate = 100 - compressed_length / initial_length * 100

    return size_different, rate


def __resolve_restored_filename(input_filename):
    dir, filename = os.path.split(input_filename)
    file, ext = os.path.splitext(filename)
    if ext == '.hfm':
        file, ext = os.path.splitext(file)
    name = os.path.join(dir, file + ext)
    i = 1
    while os.path.exists(name):
        name = os.path.join(dir, file + f'-({i})' + ext)
        i += 1
    return name
