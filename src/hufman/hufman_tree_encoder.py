from typing import List, BinaryIO, Tuple

import math

from src.hufman.dto.tree_node import TreeNode

"""
| 0000_0000__0000_0000 | 0__0_0000_0000__0_0000_0000 | 1__0_0000_0000__1_1111_1100 |
|----------------------|-----------------------------|----------------------------:|
| 16                   |                          19 | 19                          |
| count of tree nodes  | tree node with childs       | tree node with data         |
|                      |                             |                             |


| 0            | 0_0000_0000    |             0_0000_0000 |
|--------------|----------------|------------------------:|
| is data node | left child num | right child num or data |
|              |                |                         |
"""


def write_tree_to_file(root: TreeNode, io: BinaryIO) -> None:
    bts = tree_to_bytes(root)
    io.write(bts)


def tree_to_bytes(tree: TreeNode) -> bytes:
    nodes = tree.tree_to_list()
    strs = [bin(len(nodes))[2:].zfill(16)]
    for node in nodes:
        buffer = 0
        if node.character is not None:
            buffer = buffer | 1 << 18 | node.character
        else:
            if node.left_child:
                buffer = buffer << 9 | nodes.index(node.left_child)
            if node.right_child:
                buffer = buffer << 9 | nodes.index(node.right_child)
        strs.append(bin(buffer)[2:].zfill(19))

    bin_str = ''.join(strs)
    actual_bits_count = len(bin_str)
    needed_bits_count = math.ceil(actual_bits_count / 8) * 8
    bin_str = bin_str + '0' * (needed_bits_count - actual_bits_count)
    return bytes(int(bin_str[i: i + 8], 2) for i in range(0, len(bin_str), 8))


def read_tree_from_file(io: BinaryIO) -> TreeNode:
    node_count = int.from_bytes(io.read(2), 'big')
    data_length = math.ceil(node_count * 19 / 8)
    tree_data = io.read(data_length)
    return read_tree_from_bytes(node_count, tree_data)


def read_tree_from_bytes(nodes_count: int, data: bytes) -> TreeNode:
    actual_bits_count = 19 * nodes_count
    needed_bits_count = math.ceil(actual_bits_count / 8) * 8
    bin_str = bin(int.from_bytes(data, 'big') >> (needed_bits_count - actual_bits_count))[2:].zfill(actual_bits_count)
    nodes_data = []
    for i in range(0, nodes_count):
        node_bits = bin_str[i*19: i*19 + 19]
        d = {
            'is_data': node_bits[:1] == '1',
            'left_byte': int(node_bits[1:10], 2),
            'right_byte': int(node_bits[10:], 2)
        }
        nodes_data.append(d)
    return build_tree_from_data(nodes_data)


def build_tree_from_data(nodes_data: List[dict], index=0) -> TreeNode:
    node = TreeNode()
    node_data = nodes_data[index]
    if node_data.get('is_data', False):
        node.character = node_data.get('right_byte')
    else:
        if node_data.get('left_byte') > 0:
            node.left_child = build_tree_from_data(nodes_data, node_data['left_byte'])
        if node_data.get('right_byte') > 0:
            node.right_child = build_tree_from_data(nodes_data, node_data['right_byte'])
    return node
