class Node(object):
    def __init__(self, data, next = None):
        self.data = data
        self.next = next

class SSL(object):
    def __init__(self):
        self.head = None
        self.size = 0
    
    def addToFront(self, data):
        temp = Node(data)
        temp.next = self.head
        self.head = temp
        self.size += 1
        
mylist = SSL() #create list
mylist.addToFront(5) #add 5 as the new first item in the list
mylist.addToFront(3) #add 3 as the new first item, the list now contains {3, 5}

cursor = mylist.head #point to the first item (the head) of the list
while cursor != None: #print the list
    print(cursor.data)
    cursor = cursor.next

cursor = mylist.head
while cursor.next is not None: #find the last item in the list
    cursor = cursor.next

