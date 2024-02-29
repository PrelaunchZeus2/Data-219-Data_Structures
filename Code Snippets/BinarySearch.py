class Node(object):
    def __init__(self, data, next = None):
        self.data = data
        self.left = None
        self.right = None
    
class BST(object):
    def __init__(self):
        self.root = None
        self.size = 0
        self.height = 0
        #shallow trees generally perform better than deep trees
        
    def insert(self, data):
        """This function inserts a new node into the BS Tree.
        @param data: The data for the new node."""
        temp = Node(data)
        if self.root == None: #tree is empty
            self.root = temp
            self.size += 1
            self.height = 0
        else: #tree is not empty
            cursor = self.root
            while cursor != None: #navigate to find the nodes with no children
                if cursor.data > data: #go left
                    cursor = cursor.left
                elif cursor.data > data #go right
                    cursor = cursor.right
                else: #duplicate data
                    return
            #we are at the end of the branch in the right place to insert the new node
            #while loop escapes when cursor is None after checking data in last node
            cursor = temp
            self.size += 1
            self.height = self.getHeight()
            
    def getHeight(self):
        """This function calculates and returns the height of thee tree.
        @return: The height of the tree."""
        pass
        
    def search(self, data):
        """This function searches for a node in the BS Tree.
        @param data: The data to search for."""
        cursor = self.root
        while cursor != None:
            if cursor.data == data:
                return True
            elif cursor.data > data:
                cursor = cursor.left
            else:
                cursor = cursor.right
        return False
                