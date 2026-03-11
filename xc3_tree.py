
class Node:
    def __init__(self, deg):
        self._children = []
        self._deg = deg

    @property
    def children(self):
        return self._children

    @property
    def deg(self):
        return self._deg

    @deg.setter
    def deg(self, new_deg):
        self._deg = new_deg
    
    def add_child(self, new_child):
        self._children.append(new_child)

class XC3Tree:
    def __init__(self, deg):
        self._root = XC3Tree._build_tree(deg)
        self._deg = deg

    @property
    def deg(self):
        return self._deg

    @classmethod
    def _build_tree(cls, deg):
        node = Node(deg)
        for i in range(1, deg + 1):
            if i <= 2:
                node.add_child(Node(0))
            else:
                node.add_child(cls._build_tree(i - 2))
        return node

    def _height_helper(self, node):
        if not node.children:
            # node.children is an empty list
            return 0
        return 1 + max([self._height_helper(child) for child in node.children])

    @property
    def height(self):
        return self._height_helper(self._root) 

    def _nodes_num_helper(self, node):
        return 1 + sum([self._nodes_num_helper(child) for child in node.children])
    
    @property
    def nodes_num(self):
        return self._nodes_num_helper(self._root)

