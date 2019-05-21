from heapq import *
from collections import defaultdict

from src.hufman.dto.tree_node import TreeNode


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


def compress_bytes(raw_bytes: bytes, code_table: dict) -> bytes:
    return bytes([code_table[byte] for byte in raw_bytes])


if __name__ == '__main__':
    data = b'\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01' \
           b'\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02' \
           b'\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03\x03' \
           b'\x04\x04\x04\x04\x04' \
           b'\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05\x05' \
           b'\x07\x07\x07\x07\x07\x07\x07\x07\x07\x07'
    byte_nodes = create_byte_nodes(data)
    code_tree = create_code_tree(byte_nodes)
    code_table = eject_code_table(code_tree)
    # print(code_table)
    # for k, v in code_table.items():
    #     print(f'{k:b} --- {v:b}')

    print(data)
    print(compress_bytes(data, code_table))
