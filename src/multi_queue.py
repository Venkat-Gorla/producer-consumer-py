import threading
from collections import deque

class MultiQueue:
    """
    A monitor-style implementation of the Producer-Consumer problem using condition variables.

    This class provides a thread-safe queue with built-in synchronization using `threading.Condition`.
    It ensures that:
    - Producers wait if the queue is full before adding an item.
    - Consumers wait if the queue is empty before removing an item.
    - Both operations are performed atomically under a lock.

    This solution is similar to a "Monitor" because:
    1. It **encapsulates both locking and condition variables** in a single object.
    2. It **provides mutual exclusion** (ensuring only one thread modifies the queue at a time).
    3. It **handles waiting and signaling** (allowing threads to wait until conditions are met).

    Attributes:
        capacity (int): Maximum number of items the queue can hold.
        items (deque): A double-ended queue to store items.
        not_full (Condition): Condition variable to signal when the queue is not full.
        not_empty (Condition): Condition variable to signal when the queue is not empty.
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Queue capacity must be greater than 0")

        self.capacity = capacity
        self.items = deque()
        lock = threading.Lock()
        self.not_full = threading.Condition(lock)
        self.not_empty = threading.Condition(lock)

    def add_item(self, item):
        with self.not_full:
            while len(self.items) >= self.capacity:
                self.not_full.wait()

            self.items.append(item)
            self.not_empty.notify_all()

    def remove_item(self):
        with self.not_empty:
            while len(self.items) == 0:
                self.not_empty.wait()

            item = self.items.popleft()
            self.not_full.notify_all()
            return item

    def try_add_item(self, item):
        """
        Attempts to add an item without blocking.
        Returns True if successful, False if the queue is full.
        """
        with self.not_full:
            if len(self.items) >= self.capacity:
                return False
            self.items.append(item)
            self.not_empty.notify_all()
            return True

    def try_remove_item(self):
        """
        Attempts to remove an item without blocking.
        Returns the item if successful, or None if the queue is empty.
        """
        with self.not_empty:
            if len(self.items) == 0:
                return None
            item = self.items.popleft()
            self.not_full.notify_all()
            return item
