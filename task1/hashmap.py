from typing import Any, Hashable


class Node:
    """
    A class used for avoiding collisions in a hashmap via separate chaining strategy
    """

    def __init__(self, key: Hashable, value: Any):
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    """
    A class that implements a hashmap functionality

    Attributes
    ----------
    size : int
        size of the hashmap list (default 256)
    table: list
        list of bucket nodes (None | Node objects)

    Methods
    -------
    get(self, key: Hashable)
        Returns the requested key value or None if the key does not exists
    put(self, key: Hashable, value: Any)
        Updates the table node with new Node(key, value) object if one exists othewise creates one
    remove(self, key: Hashable)
        Removes node object with passed key from the table if one exists
    """

    def __init__(self, size: int = 256):
        self.size = size
        self.table = [None for _ in range(size)]

    def get(self, key: Hashable):
        # Using hash function to create a unordered hashmap
        # mod by size to avoid out of index error
        index = hash(key) % self.size

        # return None if index does not exist
        if self.table[index] is None:
            return None

        node = self.table[index]

        # search through the nodes and return if passed key exists otherwise return None
        while node.key != key and node.next is not None:
            node = node.next

        return node.value if node.key == key else None

    def put(self, key: Hashable, value: Any):
        new_node = Node(key, value)

        # using hash function to create a unordered hashmap
        # mod by size to avoid out of index error
        index = hash(key) % self.size
        cur_node = self.table[index]

        # create a new node if one does not exist
        if cur_node is None:
            self.table[index] = new_node
            return None

        # update a node value with passed data or create a new node if collision happend
        while cur_node.key != key and cur_node.next is not None:
            cur_node = cur_node.next

        if cur_node.key == key:
            cur_node.value = value
        else:
            cur_node.next = new_node

    def remove(self, key: Hashable) -> None:
        # Using hash function to create a unordered hashmap
        # mod by size to avoid out of index error
        index = hash(key) % self.size

        # skip if index does not exists
        if self.table[index] is None:
            return None

        curr_node = prev_node = self.table[index]

        # remove node if current node key equals passed key
        if curr_node.key == key:
            self.table[index] = curr_node.next
            return

        curr_node = curr_node.next

        # search through the nodes and remove node with passed key or pass if one does not exist
        while curr_node is not None:
            if curr_node.key == key:
                prev_node.next = curr_node.next
                break
            else:
                prev_node, curr_node = curr_node, curr_node.next
