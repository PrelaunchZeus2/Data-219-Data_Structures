# Heaps
#widly used for sorting purposes

# Max heap has the property that for every node i other than the root
# A[parent(i)] >= A[i]
# A min heap has the property that for every node i other than the root
# A[parent(i)] <= A[i]

#in a bst the maximum value is the right most value
#in a max heap the maximum value is the root, vice versa for min heap

import heapq

#create a list 
mylist = [1, 2, 3, 44, 23, 15, 7, 10]

#Transform list into heap
heapq.heapify(mylist)

#Print the heap
print ("Heap: ",(list(mylist)))

#heappush() inserts values into the heap.
heapq.heappush(mylist, 37)

#heappull() removes values from the heap.
heapq.heappop(mylist, 44)

print("heap after changes:", (list(mylist)))

#Heap internal accessors
#Parent return abolute i/2
#Left child return 2i
#Right child return 2i + 1


#W/O Heapify
class Heap:
    def __init__(self):
        self.heap = []
        
    def build_heap(self, data):
        """This function takes a set of nodes and build it into a heap using the heapify function.
        @param data, the data to be built into a heap."""
        self.heap = data[:]
        for i in range(len(self.heap)// 2, -1, -1):
            self.heapify(i)
            
    def heapify(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left < len(self.heap) and self.heap[left].score_difference > self.heap[largest].score_difference:
            largest = left
        if right < len(self.heap) and self.heap[right].score_difference > self.heap[largest].score_difference:
            largest = right
        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self.heapify(largest)
            
    def search(self, value):
        """This function searchees for a node with a specific value in the heap, it will return the node if found or None if not found.
        @param value, the value to bee search for in the heap
        @return the nodee with the value or None."""
        
    def get_max(self):
        """This function return the root node of the heap which is the maximum value."""
        return self.heap[0]


