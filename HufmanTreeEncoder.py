from typing import List

from dto.tree_node import TreeNode


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
    nodes_datas = []
    data_int = int(data)
    for i in range(0, 17 * nodes_count, 17):
        node_bits = data_int & 0b1_1111_1111_1111_1111
        data_int = data_int >> 17

        right_child_bits = node_bits & 0b1111_1111
        data_int = data_int >> 8
        left_child_bits = node_bits & 0b1111_1111
        data_int = data_int >> 8
        is_data = _bit = data_int & 0b1
        nodes_datas.insert(0, {
            'is_data': is_data > 0,
            'left_byte': int(left_child_bits),
            'right_byte': int(right_child_bits)
        })
    return build_tree_from_data(nodes_datas)


def build_tree_from_data(nodes_data: List[dict], index=0) -> TreeNode:
    node = TreeNode()
    node_data = nodes_data[index]
    if node_data.get('is_data'):
        node.character = build_tree_from_data(nodes_data, node_data.get('right_byte'))
    else:
        node.left_child = build_tree_from_data(nodes_data, node_data.get('left_byte'))
        node.right_child = build_tree_from_data(nodes_data, node_data.get('right_byte'))
    return node


root = TreeNode(
    left_child=TreeNode(
        left_child=TreeNode(character=255),
        right_child=TreeNode(character=254)
    ),
    right_child=TreeNode(
        left_child=TreeNode(
            left_child=TreeNode(character=253),
            right_child=TreeNode(character=252)
        )
    )
)

if __name__ == '__main__':
    with open('C:/W/controlsSystemOptimisationMethods/dto/out.hfm', 'wb') as file:
        file.write(tree_to_bytes(root))
