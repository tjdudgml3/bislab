# size = int(input())
size1 = int(input())
a = float(input())

class Node():
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next
        
# print(Node.data)

def get_hash(key, size):
    # print("_---------------")
    # print(key, size, a)
    result = int((key*a - (key*a//1) *1)*size)
    # print(result)
    return result
    

def find(key, table):
    # print(table)
    temp = table[get_hash(key, size1)]
    # print(temp)
    # if not temp.data:
    #     return temp
    # print(temp)
    cur_node = temp.next
    
    while(cur_node and cur_node.data != key):
        cur_node = cur_node.next
    
    return cur_node

def insert(key, table):
    found_node = find(key, table)
    
    if not found_node:
        new_node = Node()
        temp = table[get_hash(key, size1)]
        new_node.next = temp.next
        new_node.data = key
        temp.next = new_node
        print(f"inserted : {key} in node{get_hash(key, size1)}")
    else:
        print(f"data {key} already exist")


def print_table(table):
    for a in table:
        cur_node = table[a]
        if cur_node.next:
            cur_node = cur_node.next
            while cur_node:
                print(cur_node.data, end=" ")
                cur_node = cur_node.next
        else:
            print("null", end =" ")
        print()
    # print()


def delete(key, table):
    temp = table[get_hash(key, size1)]
    # print(temp)
    # if not temp.data:
    #     return temp
    # print(temp)
    cur_node = temp.next
    pre_node = temp
    while(cur_node and cur_node.data != key):
        pre_node = cur_node
        cur_node = cur_node.next
    if not cur_node:
        print(f"data {key} is not in the hash table")
    else:
        print(f"Deletion Success data = {key}")
        # print(pre_node.data, cur_node.data)
        pre_node.next = cur_node.next

hash_table = {}

for i in range(size1):
    hash_table[i] = Node() 
    
while(True):
    input_data = input().split(" ")
    if input_data[0] == "i":
        insert(int(input_data[1]), hash_table)
    elif input_data[0] == "d":
        delete(int(input_data[1]), hash_table)
    elif input_data[0] == "f":
        if find(int(input_data[1]), hash_table):
            print(f" found {input_data[1]} : {get_hash(int(input_data[1]), size1)}")
        else:
            print("data {} is not in the hash table".format(input_data[1]))
    elif input_data[0] == "p":
        print_table(hash_table)    
    elif input_data[0] == "q":
        break    