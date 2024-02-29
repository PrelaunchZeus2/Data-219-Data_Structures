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
                elif cursor.data > data: #go right
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
    
    def remove(self, data):
        """This function removes a node from the BS Tree.
        @param the data of the node to remove"""
        pass
        #find node
        #check if node has children
        #if no children set node above.left/right to None
        #if it only has one just copy next node to node above right or left then remove the node.
        #if it has 2 children you need to use minimal reordering principals to find a suitable candidate node (one of the children)
        #to replace the node that is being removed.
        #update size and height
        
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
    
def inOrderWalk(n):
    """This function performs an in-order walk of the tree."""
    if n == None: 
        return
        
    inOrderWalk(n.left)
    print(n.data)
    inOrderWalk(n.right)
        
    
                