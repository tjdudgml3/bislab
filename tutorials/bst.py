#Binary Search Tree

class Node():
    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

def insert(data, root):
    node = Node(data)
    cur_node = root
    if root == None:
        root = node
        return root 
    while(True):
        # if cur_node == None:
        #     cur_node = Node(data)
        #     return root
        if data > cur_node.data:
            if cur_node.right == None:
                cur_node.right = node
                return root
            cur_node = cur_node.right
        elif data < cur_node.data:
            if cur_node.left == None:
                cur_node.left = node
                return root
            cur_node = cur_node.left
        else:
            print("Element already exist")
            return root

def find(data, root):
    if root == None:
        print("Tree is empty")
        return 
    cur_node = root
    while(True):
        if cur_node == None:
            print(f"{data} is not in the tree")
            return root
        if data == cur_node.data:
            print(f"{data} is in the tree")
            return root
        if data > cur_node.data:
            cur_node = cur_node.right
        elif data < cur_node.data:
            cur_node = cur_node.left
            
def find_min(root):
    cur_node = root
    while(cur_node.left):
        cur_node = cur_node.left
    return cur_node

def delete(data, root):
    cur_node = root
    temp = 0
    if cur_node == None:
        print("Element not found")
        return root
    elif data < cur_node.data:
        cur_node.left = delete(data, cur_node.left)
    elif data > cur_node.data:
        cur_node.right = delete(data, cur_node.right)
    elif cur_node.left and cur_node.right:
        temp = find_min(cur_node.right)
        cur_node.data = temp.data
        cur_node.right = delete(cur_node.data, cur_node.right)
    else:
        temp = cur_node
        if cur_node.left == None:
            cur_node = cur_node.right
        elif cur_node.right == None:
            cur_node = cur_node.left
    return cur_node

def print_preorder(node):
    if node:
        print(node.data, end=" ")
        print_preorder(node.left)
        print_preorder(node.right)
        
def print_inorder(node):
    if node:
        
        print_inorder(node.left)
        print(node.data, end=" ")
        print_inorder(node.right)  
        
def print_postorder(node):
    if node:

        print_postorder(node.left)
        print_postorder(node.right)
        print(node.data, end=" ")  
        
        
# root = None

# while(True):
#     input_data = input().split(" ")
#     if input_data[0] == "i":
#         root = insert(int(input_data[1]),root) 
#     elif input_data[0] == "d":
#         root = delete(int(input_data[1]),root)
#     elif input_data[0] == "f":
#         root = find(int(input_data[1]),root)
#     elif input_data[0] == "pi":
#         print_inorder(root)
#         print()
#     elif input_data[0] == "pr":
#         print_preorder(root)
#         print()
#     elif input_data[0] == "po":
#         print_postorder(root)
#         print()
#     else:
#         exit()    

# root = insert(6,root)
# root =insert(4,root)
# root =insert(5,root)
# root =insert(9,root)
# root =insert(2,root)
# root = delete(2,root)
# root =insert(8,root)
# # print(root.data)
# print_preorder(root)
# print()
# print_inorder(root)
# print()
# print_postorder(root)
# print()
# # cur_node = root            
# # while(cur_node != None):
# #     print(cur_node.data)
# #     if cur_node.left:
# #         cur_node = cur_node.left
# #     else:
# #         cur_node = cur_node.right
# find(1,root)            
    
    