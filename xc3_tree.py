class Node: #LOOK HERE
    """
    Node for the XC3-Tree
    """

    def __init__(self, deg):
        self._children = []
        self._deg = deg

    @property
    def children(self):
        """
        Gets the _children property
        """
        return self._children

    @property
    def deg(self):
        """
        Gets the _deg property
        """
        return self._deg

    @deg.setter
    def deg(self, new_deg):
        """
        Sets the _deg property
        """
        self._deg = new_deg
    
    def add_child(self, new_child):
        """
        Adds a new_child to the Node
        """
        self._children.append(new_child)

class XC3Tree: #LOOK HERE
    """"
    Implementation for the XC3-Tree
    """

    def __init__(self, deg):
        self._root = XC3Tree._build_tree(deg)
        self._deg = deg

    @property
    def deg(self):
        """
        Gets the _deg property
        """
        return self._deg

    @classmethod
    def _build_tree(cls, deg):
        """
        Builds the tree from root recursively

        This method follows all the given requirments for
        a valid XC3-Tree as per described in the given instructions
        """
        node = Node(deg)
        for i in range(1, deg + 1):
            if i <= 2:
                node.add_child(Node(0))
            else:
                node.add_child(cls._build_tree(i - 2))
        return node

    def _height_helper(self, node):
        """
        Helper function to calc the height of the tree
        """
        if not node.children:
            # node.children is an empty list
            return 0
        return 1 + max([self._height_helper(child) for child in node.children])

    @property
    def height(self):
        """
        Gets the height of the tree
        """
        return self._height_helper(self._root) 

    def _nodes_num_helper(self, node):
        """
        Helper function to count the number of nodes in the tree
        """
        return 1 + sum([self._nodes_num_helper(child) for child in node.children])
    
    @property
    def nodes_num(self):
        """
        Gets the number of nodes in the tree
        """
        return self._nodes_num_helper(self._root)

