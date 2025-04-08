import unittest
from src.multi_queue import MultiQueue
import threading
import time
from typing import List

class TestMultiQueue(unittest.TestCase):
    def test_single_producer_consumer(self):
        queue = MultiQueue(2)
        input_elements = list(range(5))
        results: List[int] = []

        # should be packaged inside an object that can be used in multiple tests
        def producer():
            for i in input_elements:
                queue.add_item(i)
                time.sleep(0.1)  # Simulate processing time

        def consumer():
            for _ in input_elements:
                item = queue.remove_item()
                results.append(item)
                time.sleep(0.2)  # Simulate processing time

        producer_thread = threading.Thread(target=producer)
        consumer_thread = threading.Thread(target=consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        self.assertEqual(results, input_elements)  # Ensure all items are consumed in order

if __name__ == "__main__":
    unittest.main()
