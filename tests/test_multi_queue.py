import unittest
from src.multi_queue import MultiQueue
from tests.test_helpers import ProducerConsumerTest

class TestMultiQueue(unittest.TestCase):
    def test_single_producer_consumer(self):
        queue = MultiQueue(2)
        input_elements = list(range(5))

        test = ProducerConsumerTest(queue, input_elements)
        results = test.run()

        self.assertEqual(results, input_elements)  # Ensure all items are consumed in order

if __name__ == "__main__":
    unittest.main()
