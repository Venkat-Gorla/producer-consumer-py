import unittest
import threading
import time
from typing import List

class TestMultiQueue(unittest.TestCase):
    def test_single_producer_consumer(self):
        queue = MultiQueue(2)
        results: List[int] = []

        # should be packaged inside an object that can be used in multiple tests
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
