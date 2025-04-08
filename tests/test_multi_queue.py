from src.multi_queue import MultiQueue
from tests.producer_consumer_test import ProducerConsumerTest
from tests.try_producer_consumer_test import TryProducerConsumerTest

def test_producer_consumer():
    queue = MultiQueue(2)
    input_elements = list(range(5))

    test_harness = ProducerConsumerTest(queue, input_elements)
    consumed_elements = test_harness.run()

    assert consumed_elements == input_elements

def test_try_producer_consumer():
    queue = MultiQueue(2)
    input_data = [1, 2, 3, 4]
    test_runner = TryProducerConsumerTest(queue, input_data)
    produced, consumed = test_runner.run()

    assert produced == input_data
    assert consumed == input_data
