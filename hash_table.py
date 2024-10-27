# hash_table.py

class Node:
    """
    Represents a node in a linked list for chaining in the hash table.
    """

    def __init__(self, key, value):
        self.key = key  # Key for hashing (package_id)
        self.value = value  # The Package object
        self.next = None  # Pointer to the next node


class HashTable:
    """
    Custom hash table implementation using chaining for collision handling.
    """

    def __init__(self, size=40):
        self.size = size  # Size of the hash table
        self.table = [None] * self.size  # Initialize the table with empty buckets

    def _hash(self, key):
        """
        Hash function to compute the index for a given key.
        """
        return int(key) % self.size

    def insert(self, key, value):
        """
        Inserts a package into the hash table.
        """
        index = self._hash(key)  # Compute hash index
        new_node = Node(key, value)  # Create a new node for the package

        if self.table[index] is None:
            # No collision, insert directly
            self.table[index] = new_node
        else:
            # Collision occurred, use chaining
            current = self.table[index]
            while current.next is not None:
                if current.key == key:
                    # Update existing package
                    current.value = value
                    return
                current = current.next
            if current.key == key:
                # Update existing package
                current.value = value
            else:
                current.next = new_node

    def lookup(self, key):
        """
        Retrieves a package from the hash table by its key.
        """
        index = self._hash(key)  # Compute hash index
        current = self.table[index]  # Access the bucket at the index

        while current is not None:
            if current.key == key:
                return current.value  # Return the Package object
            current = current.next

        return None  # Package not found

    def update_status(self, key, status, delivery_time=None):
        """
        Updates the delivery status and time of a package.
        """
        package = self.lookup(key)
        if package:
            package.status = status
            package.delivery_time = delivery_time
        else:
            print(f"Package ID {key} not found.")

    def print_all_packages(self):
        """
        Prints all packages stored in the hash table.
        """
        for bucket in self.table:
            current = bucket
            while current is not None:
                print(current.value)
                current = current.next
