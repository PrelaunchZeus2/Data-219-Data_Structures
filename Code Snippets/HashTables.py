def hashFunction(x):
    """Example Hash function that returns the remainder of x divided by 2 as the index"""
    return x % 2


class HashTable(object):
    def put(self, key, value):
        pass
    
    def get(key):
        pass
        
#An ideal hash function does two things: 1. Large range of values 2. Evenly distributes values for all possible keys
#Both of which will reduce the chances of colllisions.
#If a hash value returned is larger than the array the hash functiioon can compress the value to fit the array.
#The very top function would be terrible because it fails both of these criteria.
#Its impossible to prove a perfect distriibution forr all possible keys but there exist some good "generic" hash functions that are good for most cases.

