max_heap = 9999
tree = []

def isFull(tree):
    if len(tree) == max_heap:
        return True
    else:
        return False

#insert 함수. tree의 맨뒤에 요소를 #으로 함으로써 index out of range 오류를 막는다.
def insert(data, tree):
    if len(tree) == 0:
        tree.append(data)
        tree.append("#")
        # print(tree)
        return tree
    if isFull(tree):
        print("heap is full")
        return tree
    i = len(tree) -1
    while(tree[i//2] < data):
        if i == 0:
            break
        tree[i] = tree[i//2]
        i //= 2
        
    tree[i] = data
    tree.append("#")
    # print(tree)
    return tree

def delete_root(tree):
    if len(tree) == 0:
        print("Delete :  Max Heap is empty")
        return
    max_element = tree[0]
    last_element = tree[len(tree)-2]
    i = 0
    child = 0
    while(i*2 <= len(tree) -1):
        child = i*2 + 1
        # print(f" i = {i}, chile = {child}, tree[i]= {tree[i]}, tree[child] = {tree[child]}")
        if child >= len(tree) - 2:
            break
        if child != len(tree)-1 and tree[child+1] > tree[child]:
            child += 1
        if last_element < tree[child]:
            tree[i] = tree[child]
        else:
            break
        i = child
    tree[i] = last_element
    
    #요소의 마지막을 #으로 만들어주기위한 과정
    tree.pop()
    tree.pop()
    tree.append("#")
    # print(tree)
    return tree

while(True):
    data = input().split(" ")
    if data[0] == "n":
        max_heap = int(data[1]) + 1 #+1을 하는이유 : 마지막원소를 #으로 대체하기때문
    elif data[0] == "i":
        insert(int(data[1]),tree)
    elif data[0] == "d":
        delete_root(tree)
    elif data[0] == "p":
        if len(tree) == 0:
            print("print : Max Heap is empty")
            continue
        for a in range(len(tree)-1):
            print(tree[a], end=" ")
        print("")
            
delete_root(tree)    
insert(5,tree)
insert(12,tree)
insert(35,tree)
delete_root(tree)
insert(1,tree)
insert(29,tree)
insert(50,tree)

insert(9,tree)
delete_root(tree)
insert(24,tree)
