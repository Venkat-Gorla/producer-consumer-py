import unittest
import threading
import time
from collections import deque
from typing import List

class MultiQueue:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = deque()
        
        lock = threading.Lock()  # Local lock
        self.not_empty = threading.Condition(lock)
        self.not_full = threading.Condition(lock)

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

class TestMultiQueue(unittest.TestCase):
    def test_single_producer_consumer(self):
        queue = MultiQueue(2)
        results: List[int] = []
        
        def producer():
            for i in range(5):
                queue.add_item(i)
                time.sleep(0.1)  # Simulate processing time
        
        def consumer():
            for _ in range(5):
                item = queue.remove_item()
                results.append(item)
                time.sleep(0.2)  # Simulate processing time

        producer_thread = threading.Thread(target=producer)
        consumer_thread = threading.Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        # this is wrong, should never use sorted to validate the results
        # vegorla, add this to experience, incorrect test case
        self.assertEqual(sorted(results), [0, 1, 2, 3, 4])  # Ensure all items are consumed in order

if __name__ == "__main__":
    unittest.main()
