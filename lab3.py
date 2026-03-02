testw1 = False
w1e1 = True
w1e2 = True
#######
# BST #
#######
from dataclasses import dataclass
from typing import Optional, List

class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None

def bst_insert(root: Optional[Node], key: int) -> Node:
    """Insert key into BST (ignores duplicates). Returns the root."""
    if root is None:
        return Node(key)

    cur = root
    while True:
        if key == cur.key:
            return root  # ignore duplicate
        elif key < cur.key:
            if cur.left is None:
                cur.left = Node(key)
                return root
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = Node(key)
                return root
            cur = cur.right

def height(node: Optional[Node]) -> int:
    """
    Height in edges:
    - empty tree = -1
    - single node = 0
    """
    if node is None:
        return -1
    return 1 + max(height(node.left), height(node.right))

def left_rotate(x: Optional[Node]) -> Optional[Node]:
    if x is None or x.right is None:
        return x
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    return y

def right_rotate(y: Optional[Node]) -> Optional[Node]:
    if y is None or y.left is None:
        return y
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    return x

#######
# RBT #
#######
class RBNode:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.colour = "R"

    def get_uncle(self):
        return 

    def is_leaf(self):
        return self.left == None and self.right == None

    def is_left_child(self):
        return self == self.parent.left

    def is_right_child(self):
        return not self.is_left_child()

    def is_red(self):
        return self.colour == "R"

    def is_black(self):
        return not self.is_red()

    def make_black(self):
        self.colour = "B"

    def make_red(self):
        self.colour = "R"

    def get_brother(self):
        if self.parent.right == self:
            return self.parent.left
        return self.parent.right

    def get_uncle(self):
        return self.parent.get_brother()

    def uncle_is_black(self):
        if self.get_uncle() == None:
            return True
        return self.get_uncle().is_black()

    def __str__(self):
        return "(" + str(self.value) + "," + self.colour + ")"

    def __repr__(self):
         return "(" + str(self.value) + "," + self.colour + ")"

    def rotate_right(self):
        l = self.left
        self.left = l.right

        if (l.left):
            self.l.parent = self
        l.parent = self.parent

        if(not self.parent):
            self.root = l
        elif (self.value == self.parent.left):
            self.parent.left = l
        else:
            self.parent.right = l
        l.right = self.value
        self.parent = l            

    def rotate_left(self):
        right = self.right
        self.right = right.left

        if (self.right):
            self.right.parent = self
        right.parent = self.parent

        if (not self.parent): self.root = right

        elif (self.is_left_child()): self.parent.left = right
        
        else: self.parent.right = right

        right.left = self
        self.parent = right



class RBTree:

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root == None

    def get_height(self):
        if self.is_empty():
            return 0
        return self.__get_height(self.root)

    def __get_height(self, node):
        if node == None:
            return 0
        return 1 + max(self.__get_height(node.left), self.__get_height(node.right))

    def insert(self, value):
        if self.is_empty():
            self.root = RBNode(value)
            self.root.make_black()
        else:
            self.__insert(self.root, value)

    def __insert(self, node, value):
        if value < node.value:
            if node.left == None:
                node.left = RBNode(value)
                node.left.parent = node
                self.fix(node.left)
            else:
                self.__insert(node.left, value)
        else:
            if node.right == None:
                node.right = RBNode(value)
                node.right.parent = node
                self.fix(node.right)
            else:
                self.__insert(node.right, value)

    def fix(self, node):
        if node.parent == None:
            node.make_black()

        parent_pt = None
        grand_parent_pt = None

        while node != None and node.parent != None and node.parent.is_red(): 
            parent_pt = node.parent
            grand_parent_pt = node.parent.parent
            
            # Case A:
            # Node's parent is the left child of its grand parent
            if (parent_pt == grand_parent_pt):
                uncle_pt = grand_parent_pt.right
                
                # Case 1 
                # The uncle of node is also red
                if (uncle_pt != None and uncle_pt.colour == "R"):
                    grand_parent_pt.colour = "R"
                    parent_pt.colour = "B"
                    uncle_pt.colour = "B"
                    node = grand_parent_pt
                
                else:
                    # Case 2
                    # Node is the right child of its parent
                    # We need to rotate left
                    if (node == parent_pt.right):
                        parent_pt.left_rotate()
                        node = parent_pt
                        parent_pt = node.parent

                    # Case 3
                    # Node is the left child of its parent
                    # We need to rotate right
                    grand_parent_pt.right_rotate()
                    c = parent_pt.colour
                    parent_pt.colour = grand_parent_pt.colour
                    grand_parent_pt.colour = c
                    node = parent_pt
                    
            else:
                # CASE B
                uncle_pt = grand_parent_pt.left

                # Case 1
                if uncle_pt != None and uncle_pt.colour == "R":
                    grand_parent_pt.colour = "R"
                    parent_pt.colour = "B"
                    uncle_pt.colour = "B"
                    node = grand_parent_pt
                else:
                    # Case 2
                    if node == parent_pt.left:
                        parent_pt.rotate_right()
                        node = parent_pt
                        parent_pt = node.parent

                    # Case 3
                    grand_parent_pt.rotate_left()
                    t = parent_pt.colour
                    parent_pt.colour = grand_parent_pt.colour
                    grand_parent_pt.colour = t
                    node = parent_pt   

            self.root.make_black()                
        
    def __str__(self):
        if self.is_empty():
            return "[]"
        return "[" + self.__str_helper(self.root) + "]"

    def __str_helper(self, node):
        if node.is_leaf():
            return "[" + str(node) + "]"
        if node.left == None:
            return "[" + str(node) + " -> " + self.__str_helper(node.right) + "]"
        if node.right == None:
            return "[" +  self.__str_helper(node.left) + " <- " + str(node) + "]"
        return "[" + self.__str_helper(node.left) + " <- " + str(node) + " -> " + self.__str_helper(node.right) + "]"

if (testw1):
    tree = RBTree()
    L = [10,8,10,15,30]
    for n in L:
        tree.insert(n)
        print(tree.__str__())


################
# Experiment 1 #
################
if w1e1:
    print("ex1")





################
# Experiment 2 #
################
if w1e2:
    print("ex2")