class HashMapNode:
    """
    A node to store a key-value pair in the hash map.

    Attributes:
        key: The key associated with the value.
        value: The value to be stored in the hash map.
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value


class CreateHashMap:
    """
    A simple implementation of a hash map
    It maps keys to values, allowing for fast retrieval of values based on their keys.

    Attributes:
        capacity (int): The total number of 'buckets' available in the hash map.
        size (int): The current number of elements stored in the hash map.
        hash_table (list): A list of lists, where each sublist represents a 'bucket' in which we store key-value pairs.
    """

    def __init__(self, initial_capacity=20):
        """
        Initializes the hash map with a specified initial capacity.

        Args:
            initial_capacity (int): The initial number of buckets in the hash map.
        """
        self.capacity = initial_capacity
        self.size = 0
        self.hash_table = [[] for _ in range(initial_capacity)]

    def _hash(self, key):
        """
        Generates a hash for a given key.

        Args:
            key: The key to hash.

        Returns:
            An integer hash value for the given key.
        """
        return hash(key) % self.capacity

    def insert(self, key, item):
        """
        Inserts a key-value pair into the hash map.

        Args:
            key: The key associated with the item.
            item: The item to be stored in the hash map.
        """
        if self.size / self.capacity > 0.7:
            self._resize()

        bucket = self._hash(key)
        bucket_list = self.hash_table[bucket]

        for node in bucket_list:
            if node.key == key:
                node.value = item
                return

        bucket_list.append(HashMapNode(key, item))
        self.size += 1

    def lookup(self, key):
        """
        Retrieves the value associated with a given key.

        Args:
            key: The key to search for in the hash map.

        Returns:
            The value associated with the key if found, otherwise None.
        """
        bucket = self._hash(key)
        bucket_list = self.hash_table[bucket]

        for node in bucket_list:
            if node.key == key:
                return node.value
        return None

    def remove(self, key):
        """
        Removes the key-value pair associated with a given key from the hash map.

        Args:
            key: The key of the pair to remove.

        Returns:
            True if removal was successful, False otherwise.
        """
        bucket = self._hash(key)
        bucket_list = self.hash_table[bucket]

        for idx, node in enumerate(bucket_list):
            if node.key == key:
                del bucket_list[idx]
                self.size -= 1
                return True
        return False

    def _resize(self):
        """
        Resizes the hash map by doubling its capacity. This is done to maintain efficient operations as the hash map grows.
        """
        self.capacity *= 2
        new_hash_table = [[] for _ in range(self.capacity)]

        for bucket_list in self.hash_table:
            for node in bucket_list:
                new_bucket = self._hash(node.key)
                new_hash_table[new_bucket].append(node)

        self.hash_table = new_hash_table