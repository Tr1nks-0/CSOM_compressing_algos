import json
from json import JSONEncoder

from encoder.hufman.tree.tree_node import Node


class TreeEncoder(JSONEncoder):
    # NAME: Sergey Baydin, 8.04.122.010.18.2
    # ASGN: N1

    def default(self, obj):
        if isinstance(obj, Node):
            if obj.is_data():
                return {'type': 'data',
                        'character': obj.character}
            else:
                return {'type': 'conn',
                        'left': obj.left_child,
                        'right': obj.right_child}
        else:
            return json.dumps(obj)
