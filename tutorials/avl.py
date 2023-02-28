# from bst import print_inorder

class Node():
    def __init__(self, data, height=-1, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.height = height
      
        
def single_rotate_left(root):
    
    cur_node = root.left
    if not cur_node:
        return root
    root.left = cur_node.right
    cur_node.right = root
    
    root.height = max(get_height(root.left), get_height(root.right)) + 1
    cur_node.height = max(get_height(cur_node.left), get_height(cur_node.right)) + 1
    
    return cur_node


def single_rotate_right(root):
    cur_node = root.right
    if not cur_node:
        return root
    root.right = cur_node.left
    cur_node.left = root
    
    root.height = max(get_height(root.left), get_height(root.right)) + 1
    cur_node.height = max(get_height(cur_node.left), get_height(cur_node.right)) + 1
    
    return cur_node


def double_rotate_left(root):
    # print("singlerotateright -------left", root.left.data)
    root.left = single_rotate_right(root.left)
    # print("singlerotateleft -------", root.data)
    return single_rotate_left(root)


def double_rotate_right(root):
    # print("singlerotateleft -------right", root.right.data)
    root.right = single_rotate_left(root.right)
    # print("singlerotateright -------", root.data)
    return single_rotate_right(root)


def get_height(node):
    if node == None:
        return -1
    else:
        return node.height
    
    
def print_inorder(node):
    if node:
        
        print_inorder(node.left)
        print(node.data, end = " ")
        print_inorder(node.right)
        
        
def insert(data, root):
    # node = Node(data)
    cur_node = root
    if root == None:
        root = Node(data)
    
    elif data < root.data:
        root.left = insert(data, root.left)
        if get_height(root.left) - get_height(root.right) == 2:
            if data < root.left.data:
                # print("singlerotateleft -------", root.data)
                root = single_rotate_left(root)
            else:
                # print("doublerotateleft -------", root.data)
                root = double_rotate_left(root)
                
    elif data > root.data:
        # print(f" input_data = {data}, root.data = {root.data}")
        
        root.right = insert(data, root.right)
        
        # print(f" after insert input_data = {data}, root.data = {root.data}")
        if get_height(root.right) - get_height(root.left) == 2:
            if data < root.right.data:
                
                # print("singlerotateright -------", root.data)
                root = single_rotate_right(root)
            else:
                
                # print("doublerotateright -------", root.data)
                root = double_rotate_right(root)
    else:
        print("data is already in the tree")
        # return root
               
    root.height = max(get_height(root.left), get_height(root.right)) + 1
    return root


root = None
    
input_data = input().split(" ")

for i in input_data:
    # print("inserting data = {}".format(int(i)))
    root = insert(int(i), root)
    print(f"height : {get_height(root)}")
    print_inorder(root)
    print()
    