import math
from collections import defaultdict
from heapq import heappop
from typing import List, Dict, BinaryIO, Tuple

from hufman.tree.tree_node import Node


def build_tree_from_bytes(data: bytes) -> Node:
    frequencies = defaultdict(int)
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
        table[node.character] = value if value else '0'
    else:
        if node.has_left_child():
            tree_to_codetable(node.left_child, table, value + '0')
        if node.has_right_child():
            tree_to_codetable(node.right_child, table, value + '1')
    return table


def tree_to_list(node: Node, list: List[Node] = None) -> list:
    if list is None:
        list = []
    list.append(node)
    if node.has_left_child():
        tree_to_list(node.left_child, list)
    if node.has_right_child():
        tree_to_list(node.right_child, list)
    return list


def tree_to_file(tree: Node, filename: str) -> None:
    with open(filename, 'wb') as file:
        tree_to_io(tree, file)


def tree_to_io(tree: Node, io: BinaryIO) -> None:
    tree_bytes = tree_to_bytes(tree)
    io.write(tree_bytes)


def tree_to_bytes(node: Node) -> bytes:
    nodes = tree_to_list(node)
    node_strs = [bin(len(nodes))[2:].zfill(16)]  # list of bin strs with first node count str
    for node in nodes:
        buffer = 0
        if node.is_data():
            buffer = 1 << 18 | node.character
        else:
            if node.left_child:
                buffer = buffer << 9 | nodes.index(node.left_child)
            if node.right_child:
                buffer = buffer << 9 | nodes.index(node.right_child)
        node_strs.append(bin(buffer)[2:].zfill(19))  # int to bin str with cutting "0b" and fill leading zero to 19 bits

    bit_str = ''.join(node_strs)
    bit_count = len(bit_str)
    reduced_bit_count = __reduce_to_bytes_bit_count(bit_count)
    bit_str = bit_str + '0' * (reduced_bit_count - bit_count)
    return bytes(int(bit_str[index:index + 8], 2) for index in range(0, len(bit_str), 8))


def tree_from_file(filename: str) -> Tuple[Node, int]:
    with open(filename, 'rb') as file:
        return tree_from_io(file)


def tree_from_io(io: BinaryIO) -> Tuple[Node, int]:
    node_count = int.from_bytes(io.read(2), 'big')
    if node_count == 0:
        return None, 0
    data_length = math.ceil(node_count * 19 / 8)
    tree_bytes = io.read(data_length)
    return tree_from_bytes(node_count, tree_bytes), node_count


def tree_from_bytes(node_count: int, data: bytes) -> Node:
    bit_count = 19 * node_count
    reduced_bit_count = __reduce_to_bytes_bit_count(bit_count)
    bit_str = bin(int.from_bytes(data, 'big') >> (reduced_bit_count - bit_count))[2:].zfill(bit_count)
    nodes_data = []
    for i in range(node_count):
        node_bits = bit_str[i * 19:i * 19 + 19]
        is_data = node_bits[0] == '1'
        left = 0 if is_data else int(node_bits[1:10], 2)
        right = int(node_bits[10:], 2)
        nodes_data.append({
            'is_data': is_data,
            'left': left,
            'right': right
        })
    return _restore_tree(nodes_data)


def _restore_tree(nodes_data: List[dict], index=0) -> Node:
    node_data = nodes_data[index]
    if node_data['is_data']:
        node = Node.data_node(node_data['right'])
    else:
        node = Node.connection_node()
        if node_data['left'] > 0:
            node.left_child = _restore_tree(nodes_data, node_data['left'])
        if node_data['right'] > 0:
            node.right_child = _restore_tree(nodes_data, node_data['right'])
    return node


def __reduce_to_bytes_bit_count(bit_count: int) -> int:
    return math.ceil(bit_count / 8) * 8
