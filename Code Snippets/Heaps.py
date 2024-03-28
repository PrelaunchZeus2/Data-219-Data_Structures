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


