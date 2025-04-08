import unittest
from src.multi_queue import MultiQueue
from tests.test_helpers import ProducerConsumerTest

class TestMultiQueue(unittest.TestCase):
    def test_single_producer_consumer(self):
        queue = MultiQueue(2)
        input_elements = list(range(5))

        test_harness = ProducerConsumerTest(queue, input_elements)
        consumed_elements = test_harness.run()

        self.assertEqual(consumed_elements, input_elements)

if __name__ == "__main__":
    unittest.main()
