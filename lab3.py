import random

testw1 = False
w1e1 = False
w1e2 = False
w2e3 = True
w2e4 = True
#######
# BST #
#######
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None

def bst_insert(root: Optional[Node], key: int) -> Node:
    """Insert key into BST. Duplicates are handled on the right. Returns the root."""
    if root is None:
        return Node(key)

    cur = root
    while True:
        if key < cur.key:
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
        if not l: return
        self.left = l.right

        # If the node has a left child
        # Make the left node the parent of the node
        if (self.left):                     #LOOK HERE
            self.left.parent = self
        l.parent = self.parent

        # If the node has a parent
        # Swap so that the parent has the new higher node (l) node
        # Accounting for whether node is the left or right child
        if (self.parent):                   #LOOK HERE
            if (self.is_left_child()):      #LOOK HERE
                self.parent.left = l
            else:                           #LOOK HERE
                self.parent.right = l

        # Fix the relation to the left node (l)
        l.right = self                      #LOOK HERE
        self.parent = l                     #LOOK HERE

    def rotate_left(self):
        r = self.right
        if not r: return
        self.right = r.left

        # If the node has a right child
        # Make the right node the parent of the node
        if (self.right):                    #LOOK HERE
            self.right.parent = self
        r.parent = self.parent

        # If the node has a parent
        # Swap so that the parent has the new higher node (r) node
        # Accounting for whether node is the left or right child
        if (self.parent):                   #LOOK HERE
            if (self.is_left_child()):      #LOOK HERE
                self.parent.left = r   
            else:                           #LOOK HERE
                self.parent.right = r

        # Fix the relation to the right node (r)
        r.left = self                       #LOOK HERE
        self.parent = r                     #LOOK HERE

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

        while node and node.parent and node.parent.is_red(): 
            parent_pt = node.parent
            grand_parent_pt = parent_pt.parent

            if grand_parent_pt is None: break
            
            # Case A:
            # Node's parent is the left child of its grand parent
            if (parent_pt == grand_parent_pt.left):
                uncle_pt = grand_parent_pt.right
                
                # Case 1 
                # The uncle of node is also red
                if (uncle_pt and uncle_pt.is_red()):
                    grand_parent_pt.make_red()
                    parent_pt.make_black()
                    uncle_pt.make_black()
                    node = grand_parent_pt
                
                else:
                    # Case 2
                    # Node is the right child of its parent
                    # We need to rotate left
                    if (node == parent_pt.right):
                        node = parent_pt
                        node.rotate_left()
                        parent_pt = node.parent

                    # Case 3
                    # Node is the left child of its parent
                    # We need to rotate right
                    parent_pt.make_black()
                    grand_parent_pt.make_red()
                    grand_parent_pt.rotate_right()
                    
            else:
                # CASE B
                # The parent of the node is the right child
                uncle_pt = grand_parent_pt.left

                # Case 1
                # The uncle of the node is red
                if uncle_pt and uncle_pt.is_red():
                    grand_parent_pt.make_red()
                    parent_pt.make_black()
                    uncle_pt.make_black()
                    node = grand_parent_pt
                else:
                    # Case 2
                    # The node is the left child
                    if node == parent_pt.left:
                        node = parent_pt
                        node.rotate_right()
                        parent_pt = node.parent

                    # Case 3
                    # The node is the right child
                    parent_pt.make_black()
                    grand_parent_pt.make_red()
                    grand_parent_pt.rotate_left()

        temp = node
        while temp.parent is not None:
            temp = temp.parent
        self.root = temp
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
    
def create_random_list(length, max_value):
    return [random.randint(0, max_value) for _ in range(length)]

def create_multiple_random_lists(amount_of_lists, max_value, length):
    return [create_random_list(length, max_value) for _ in range(amount_of_lists)]

def create_near_sorted_list(length, max_value, swaps):
    L = create_random_list(length, max_value)
    L.sort()
    for _ in range(swaps):
        r1 = random.randint(0, length - 1)
        r2 = random.randint(0, length - 1)
        swap(L, r1, r2)
    return L

def swap(L, i, j):
    L[i], L[j] = L[j], L[i]

if (testw1):
    tree = RBTree()
    L = [10,8,1000,15,30,45,70,3,9,12,8,792]
    for n in L:
        tree.insert(n)
        print(tree.__str__())

###############
# Experiments #
###############
import matplotlib
import random
import timeit
import matplotlib.pyplot as plt
import numpy as np

################
# Experiment 1 #
################
runs = 100
if w1e1:
    for _ in range(1):
        list_gen = create_random_list(1000,80)
        RBTree_gen = RBTree()

        for i in list_gen:
            RBTree_gen.insert(i)
            print(RBTree_gen.__str__())

    try:
        print(RBTree_gen.get_height())
    except:
        print("FAIL")

################
# Experiment 2 #
################
import sys
sys.setrecursionlimit(30000)
if w1e2:
    runs = 100
    length = 10000
    max_value = 100000
    swaps = [0] + [2**x for x in range(14)]
    avg_height_RBT = [0] * len(swaps)
    avg_height_BST = [0] * len(swaps)

    track = -1
    for s in swaps:
        track += 1
        for i in range(runs):
            L = create_near_sorted_list(length, max_value, s)

            RBT = RBTree()
            BST = None

            for e in L:
                RBT.insert(e)
                BST = bst_insert(BST, e)

            avg_height_BST[track] += height(BST)
            avg_height_RBT[track] += RBT.get_height()
        
        print(s)
        avg_height_BST[track] /= runs
        avg_height_RBT[track] /= runs

    plt.plot(swaps, avg_height_RBT, color="red", label="RBT")
    plt.plot(swaps, avg_height_BST, color="black", label="BST")
    plt.title("RBT vs BST Height on Near-Sorted Inserts")
    plt.xlabel('Number of Swaps')
    plt.ylabel('Height')
    current_ticks = [t for t in plt.yticks()[0] if t > 0]
    plt.yticks(current_ticks + [avg_height_RBT[0]])
    plt.legend()
    plt.savefig('Ex2_RBT_BST_Swaps.png')


from xc3_tree import XC3Tree
################
# Experiment 3 #
################
def experiment3(): #LOOK HERE
    for i in range(26): 
        print(f"An XC3 Tree of {i} deg has height: {XC3Tree(i).height}")

if w2e3:
    experiment3()

################
# Experiment 4 #
################
def experiment4(): #LOOK HERE
    for i in range(26): 
        print(f"An XC3 Tree of {i} deg has {XC3Tree(i).nodes_num} nodes")

if w2e4:
    experiment4()
