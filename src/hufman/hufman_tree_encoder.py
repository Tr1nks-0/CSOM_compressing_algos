from typing import List, BinaryIO

from src.hufman.dto.tree_node import TreeNode


def tree_to_io(root: TreeNode, io: BinaryIO) -> None:
    io.write(tree_to_bytes(root))


def tree_from_io(io: BinaryIO) -> TreeNode:
    node_count = int.from_bytes(io.read(1), 'big')
    data_length = node_count * 2 + (node_count // 8 + (1 if node_count % 8 else 0))
    tree_data = io.read(data_length)
    return read_tree_from_bytes(node_count, tree_data)


def tree_to_bytes(root: TreeNode) -> bytes:
    nodes = root.tree_to_list()
    buffer = len(nodes)
    nums = []
    for node in nodes:
        if node.is_data_node():
            buffer = buffer << 1 | 1
            buffer = buffer << 16 | node.character
        else:
            buffer = buffer << 1
            buffer = buffer << 8
            if node.left_child:
                buffer = buffer | nodes.index(node.left_child)
            buffer = buffer << 8
            if node.right_child:
                buffer = buffer | nodes.index(node.right_child)

    length = 8 + 17 * len(nodes)
    bytes_str = bin(buffer)[2:].zfill(length)
    for index in range(0, length, 8):
        sss = bytes_str[index:index + 8]
        tmp = int(sss, 2)
        nums.append(tmp)
        buffer = buffer >> 8
    return bytes(nums)


def read_tree_from_bytes(nodes_count: int, data: bytes):
    nodes_data = []
    data_int = int.from_bytes(data, 'big')
    for i in range(0, 17 * nodes_count, 17):
        node_bits = data_int & 0b1_1111_1111_1111_1111
        data_int = data_int >> 17
        right_child_bits = node_bits & 0b1111_1111
        node_bits = node_bits >> 8
        left_child_bits = node_bits & 0b1111_1111
        is_data = _bit = data_int & 0b1
        nodes_data.insert(0, {
            'is_data': is_data > 0,
            'left_byte': int(left_child_bits),
            'right_byte': int(right_child_bits)
        })
    return build_tree_from_data(nodes_data)


def build_tree_from_data(nodes_data: List[dict], index=0) -> TreeNode:
    node = TreeNode()
    node_data = nodes_data[index]
    if node_data.get('is_data', False):
        node.character = node_data.get('right_byte')
    else:
        if node_data.get('left_byte') > 0:
            node.left_child = build_tree_from_data(nodes_data, node_data.get('left_byte'))
        if node_data.get('right_byte') > 0:
            node.right_child = build_tree_from_data(nodes_data, node_data.get('right_byte'))
    return node
