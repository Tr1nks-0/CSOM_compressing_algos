from heapq import *
from collections import defaultdict

from src.hufman.dto.tree_node import TreeNode
from src.hufman.hufman_tree_encoder import write_tree_to_file, read_tree_from_file


def decompress_from_file(filename: str) -> bytearray:
    with open(filename, 'rb') as file:
        code_tree = read_tree_from_file(file)
        data_int = int.from_bytes(file.read(), 'big')
        data_bits = bin(data_int)[2:]
        data_bytes = bytearray()
        node = code_tree
        for index in range(len(data_bits)):
            bit = data_bits[index:index + 1]

            if bit == '1':
                node = node.right_child
            else:
                node = node.left_child
            if node.character is not None:
                data_bytes.append(node.character)
                node = code_tree
    return data_bytes


def compress_to_file(data: bytes, filename: str) -> None:
    byte_nodes = create_byte_nodes(data)
    code_tree = create_code_tree(byte_nodes)
    with open(filename, 'wb') as file:
        write_tree_to_file(code_tree, file)
        file.write(compress(data, code_tree))


def compress(data: bytes, code_tree: TreeNode) -> bytearray:
    code_table = code_tree.tree_to_code_table()
    temp = 0
    for byte in data:
        byte = code_table.get(byte)
        temp = temp << len(byte) | int(byte, 2)
    compressed = bytearray()
    for index in range(0, len(bin(temp)[2:]), 8):
        byte = temp & 0b1111_1111
        compressed.insert(0, byte)
        temp = temp >> 8
    return compressed


def create_byte_nodes(data: bytes) -> defaultdict:
    nodes = defaultdict(int)
    for byte in data:
        nodes[byte] += 1
    return nodes


def create_code_tree(byte_nodes: defaultdict) -> TreeNode:
    queue = []
    for byte, frequency in byte_nodes.items():
        heappush(queue, TreeNode(character=byte, frequency=frequency))

    while len(queue) > 1:
        left = heappop(queue)
        right = heappop(queue)
        tree_node = TreeNode(frequency=left.frequency + right.frequency, left_child=left, right_child=right)
        heappush(queue, tree_node)
    root = heappop(queue)
    # draw_tree(root)
    return root


def eject_code_table(code_tree_root: TreeNode) -> dict:
    table = code_tree_root.tree_to_code_table()
    return table
