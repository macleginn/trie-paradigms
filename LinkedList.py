"""This module provides an implementation of a linked list that should serve as a building block
for the Trie.py module."""


class ListNode:
    """A simple node type for a bidirectional linked list."""
    def __init__(self, previous = None, next = None, key = None, value = None):
        self.previous: ListNode = previous
        self.next: ListNode = next
        self.key: str = key
        self.value = value


class LinkedList:
    def __init__(self):
        self.head: ListNode = None
        self.size = 0

    def insertByKey(self, key, value):
        current = self.head
        previous = None
        while current is not None and current.key < key:
            previous = current
            current = current.next
        if current is None:
            # A new node is created at the end
            self.size += 1
            new = ListNode(previous, None, key, value)
            # If self.head is None, this is the first node
            if self.head is None:
                self.head = new
            else:
                previous.next = new
        elif current.key == key:
            # Replace the value
            current.value = value
        else:
            # We need to add a new node before this one
            self.size += 1
            new = ListNode(previous, current, key, value)
            current.previous = new
            if self.head.key > key:
                # This is the new head
                assert previous is None
                self.head = new
            else:
                # Backpatch the previous node
                previous.next = new


    def getByKey(self, key):
        current = self.head
        while current is not None and current.key != key:
            current = current.next
        if current is None:
            return None
        else:
            return current.value


    def keys(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.key)
            current = current.next
        return result
