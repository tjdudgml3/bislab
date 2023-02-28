class Node():
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


def MakeEmpty(header):
    pass

def IsEmpty(header):
    return header.next == None


def Islast(node, header):
    return node.next == None


def Delete(data, header):
    temp_node = None
    current = header
    temp_node = current
    current = current.next
    
    # print(current, current.next, current.data)
    while(current.data[0] != data):
        if current.next == None:
            print("data not found")
            return
        temp_node = current
        current = current.next
        # print(current.data[0], current.next, temp_node.data[0], temp_node.next)
    if Islast(current, header):
        temp_node.next = None
    else:
        temp_node.next = current.next  
    print(f"deletion Successs : {data}")   


def Find(data, header):
    current = header.next
    while(current.data[0] != data):
        if current.next == None:
            print("data Not Found")
            return
        current = current.next
    return current.data[1]
    

def Insert(id, name, header):
    current = header
    
    while current.next != None:
        current = current.next
    current.next = Node([id,name])
    print(f"Insertion Successs : {id}")


def DeleteList():
    pass


header = Node() 
id_book = []
while(True):
    command = input().split(' ')
    
    if command[0] == 'i':
        if command[1] not in id_book:
            id_book.append(command[1])
            Insert(command[1], command[2], header)
        else:
            print("id already exist")
            
    elif command[0] == 'd':
        
        if IsEmpty(header):
            print("list empty")
        else:
            if command[1] in id_book:
                Delete(command[1], header)    
                id_book.remove(command[1])
            else:
                print("id not found")
            
    elif command[0] =='f':
        print(f"name = {Find(command[1], header)}")
        
    elif command[0] == 'p':
        current = header
        # print(current.data, current.next)
        if IsEmpty(header):
            print("list empty")
        while(current.next):
            current = current.next
            print(f"student ID = {current.data[0]}, student Name = {current.data[1]}")
            
    elif command[0] == "stop":
        break
    
    else:
        print("command not found")
    