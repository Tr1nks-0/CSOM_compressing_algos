from heapq import *
from collections import defaultdict

from src.hufman.dto.tree_node import TreeNode
from src.hufman.hufman_tree_encoder import tree_to_io


def decompress_from_file() -> bytearray:
    pass


def compress_to_file(data: bytes, filename: str) -> None:
    byte_nodes = create_byte_nodes(data)
    code_tree = create_code_tree(byte_nodes)
    with open(filename, 'wb') as file:
        tree_to_io(code_tree, file)
        file.write(compress(data, code_tree))


def compress(data: bytes, code_tree: TreeNode) -> bytearray:
    code_table = code_tree.fill_code_table({})
    temp = 0
    for byte in data:
        byte = code_table.get(byte)
        temp = temp << len(bin(byte)[2:]) | byte
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
    return heappop(queue)


def eject_code_table(code_tree_root: TreeNode) -> dict:
    table = {}
    code_tree_root.fill_code_table(table)
    return table
