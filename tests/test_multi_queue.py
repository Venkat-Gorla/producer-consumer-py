import threading
import time
from typing import List
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

# this test verifies producer consumer blocking behavior with an Event and 
# minimal use of sleep
def test_producer_consumer_with_event():
    queue = MultiQueue(2)
    input_elements = list(range(5))
    producer_event = threading.Event()

    producer_thread = _produce_items_and_signal(queue, input_elements, producer_event)
    producer_event.wait()
    time.sleep(0.01)

    consumed_elements = []
    consumer_thread = _consume_items(queue, len(input_elements), consumed_elements)

    producer_thread.join()
    consumer_thread.join()

    assert consumed_elements == input_elements

def _produce_items_and_signal(
    queue: MultiQueue, 
    input_elements: List[int], 
    producer_event: threading.Event
) -> threading.Thread:
    # Ensure producer fills queue before signaling
    assert len(input_elements) > queue.capacity

    def produce_items():
        for index in range(queue.capacity):
            queue.add_item(input_elements[index])

        producer_event.set()
        for index in range(queue.capacity, len(input_elements)):
            queue.add_item(input_elements[index])

    producer_thread = threading.Thread(target=produce_items)
    producer_thread.start()
    return producer_thread

def _consume_items(
    queue: MultiQueue, 
    elements_count: int,
    consumed_elements: List[int]
) -> threading.Thread:
    def consume_items():
        for _ in range(elements_count):
            consumed_elements.append(queue.remove_item())

    consumer_thread = threading.Thread(target=consume_items)
    consumer_thread.start()
    return consumer_thread
