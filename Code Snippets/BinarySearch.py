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
            if self.root.data > data: #go left
                pass
            
            elif self.root.data < data: #go right
                pass
            
            else: #duplicate data
                pass