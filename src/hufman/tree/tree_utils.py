import math
from collections import defaultdict
from heapq import heappop
from typing import List, Dict

from hufman.tree.tree_node import Node


def build_tree_from_file(filename: str) -> Node:
    with open(filename, 'rb') as file:
        data = file.read()
    return build_tree_from_bytes(data)


def build_tree_from_bytes(data: bytes) -> Node:
    frequencies = defaultdict()
    for byte in data:
        frequencies[byte] += 1

    queue = []
    for byte, frequency in frequencies.items():
        queue.append(Node.data_node(byte, frequency))

    while len(queue) > 1:
        queue.sort()
        left = heappop(queue)
        right = heappop(queue)
        queue.append(Node.connection_node(left, right, left.frequency + right.frequency))

    return heappop(queue)


def tree_to_codetable(node: Node, table: Dict[bytes, str] = None, value: str = '') -> dict:
    if table is None:
        table = {}
    if node.is_data():
        table[node.character] = value
    else:
        if node.left_child is not None:
            tree_to_codetable(node.left_child, table, value + '0')
        if node.right_child is not None:
            tree_to_codetable(node.right_child, table, value + '1')
    return table


def tree_to_list(node: Node, list: List['TreeNode'] = None) -> list:
    if list is None:
        list = []
    list.append(node)
    if node.left_child is not None:
        tree_to_list(node.left_child, list)
    if node.right_child is not None:
        tree_to_list(node.right_child, list)
    return list


def tree_to_bytes(node: Node) -> bytes:
    nodes = tree_to_list(node)
    node_strs = [bin(len(nodes))[2:].zfill(16)]  # list of bin strs with first node count str
    for node in nodes:
        buffer = 0
        if node.is_data():
            buffer = 1 << 18 | int.from_bytes(node.character, 'big')
        else:
            if node.left_child:
                buffer = buffer << 9 | nodes.index(node.left_child)
            if node.right_child:
                buffer = buffer << 9 | nodes.index(node.right_child)
        node_strs.append(bin(buffer)[2:].zfill(19))  # int to bin str with cutting "0b" and fill leading zero to 19 bits

    bit_str = ''.join(node_strs)
    bit_count = len(bit_str)
    reduced_to_bytes_bit_count = math.ceil(bit_count / 8) * 8
    bit_str = bit_str + '0' * (reduced_to_bytes_bit_count - bit_count)
    return bytes(int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))

    # def decompress_from_file(filename: str, tree_temp) -> bytearray:
#     with open((filename + '.tree'), 'rb') as file:
#         code_tree = read_tree_from_file(file)
#         print(code_tree == tree_temp)
#         code_tree=tree_temp
#     with open(filename, 'rb') as file:
#         # code_tree = read_tree_from_file(file)
#         readed = file.read()
#         data_int = int.from_bytes(readed, 'big')
#         data_bits = bin(data_int)[2:]
#
#         data_bytes = bytearray()
#         node = code_tree
#         for index in range(len(data_bits)):
#             bit = data_bits[index:index + 1]
#
#             if bit == '1':
#                 node = node.right_child
#             else:
#                 node = node.left_child
#             if node.character is not None:
#                 data_bytes.append(node.character)
#                 node = code_tree
#     return data_bytes


# def compress_to_file(data: bytes, filename: str):
#     byte_nodes = create_byte_nodes(data)
#     code_tree = create_code_tree(byte_nodes)
#     with open((filename + '.tree'), 'wb') as file:
#         write_tree_to_file(code_tree, file)
#     with open(filename, 'wb') as file:
#         # write_tree_to_file(code_tree, file)
#         file.write(compress(data, code_tree))
#     return code_tree

# def compress(data: bytes, code_tree: TreeNode) -> bytearray:
#     code_table = code_tree.tree_to_code_table()
#     temp = 0
#     for byte in data:
#         byte = code_table.get(byte)
#         temp = temp << len(byte) | int(byte, 2)
#     compressed = bytearray()
#     for index in range(0, len(bin(temp)[2:]), 8):
#         byte = temp & 0b1111_1111
#         compressed.insert(0, byte)
#         temp = temp >> 8
#     return compressed
#
