class Node(object):
    def __init__(self, data, next = None):
        self.data = data
        self.next = next

class SLL(object):
    def __init__(self):
        self.head = None
        self.size = 0
    
    def addToFront(self, data): #add item to front of the list
        """This function adds a new node to the front of the list.
        @param data: The data for the new node."""
        temp = Node(data)
        temp.next = self.head
        self.head = temp
        self.size += 1
        
    def addToTail(self, data): #add item to the end of the list
        """This function adds a new node to the end of the list.
        @param data: The data for the new node."""
        temp = Node(data)
        if self.head == None: #check if the list is empty
            self.head = temp
            self.size += 1
        else:
            cursor = self.head
            while cursor.next != None:
                cursor = cursor.next
            cursor.next = temp
            self.size += 1
            
    def remove(self, index):
        pass
    
    def indexOf(self, data):
        """This function returns the index of the first occurrence of the data in the list.
        @param data: The data to search for.
        @return: The index of the first occurrence of the data in the list, or -1 if the data is not found."""
        cursor = self.head
        count = 0
        while cursor.data != data:
            cursor = cursor.next
            count += 1
            if cursor == None:
                return -1
        return count
    
    def size(self):
        """This function returns the number of nodes in the list
        @return: The number of nodes in the list"""
        return self.size
    
    def makeSentinel(self):
        """This function adds a Sentinel node with data -99 to the front of the list."""
        temp = Node(-99)
        temp.next = self.head
        self.head = temp
        self.size += 1
    
    def join(self, b):
        """This function joins two lists together. The list that calls this function will have the data from the second list added
        to the end of the list.
        @param b: The list to join to the end of the list that calls this function."""
        cursor = self.head
        while cursor.next != None:
            cursor = cursor.next
        pass
        

        
mylist = SLL() #create list
mylist.addToFront(5) #add 5 as the new first item in the list
mylist.addToFront(3) #add 3 as the new first item, the list now contains {3, 5}

cursor = mylist.head #point to the first item (the head) of the list
while cursor != None: #print the list
    print(cursor.data)
    cursor = cursor.next

cursor = mylist.head
while cursor.next is not None: #find the last item in the list
    cursor = cursor.next
    


