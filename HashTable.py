# Luis Ortiz #000855626


# Class to create a Hash Table for the Packages
class HashTable:

    """
    Constructor with a maximum size of 10.
    Assigns buckets with empty list
    """
    def __init__(self):
        self.size = 10
        self.arr = [[] for i in range(self.size)]

    """
    Create Hash Key
    O(1)
    """
    def get_hash(self, key):
        hash = int(key) % 10
        return hash

    """
    Insert new Package into Hash Table. Update Package if it already exists
    O(n)
    """
    def add_update(self, key, value):
        hash = self.get_hash(key)
        found = False
        for index, element in enumerate(self.arr[hash]):
            if len(element) == 2 and element[0] == key:
                self.arr[hash][index] = (key, value)
                found = True
                break
        if not found:
            self.arr[hash].append((key, value))

    """
    Search for a Package with matching key in the Hash Table.
    O(n)
    """
    def get(self, key):
        hash = self.get_hash(key)
        # return self.arr[hash]
        for element in self.arr[hash]:
            if element[0] == key:
                return element[1]
