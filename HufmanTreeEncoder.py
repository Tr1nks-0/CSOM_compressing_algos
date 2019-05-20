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
