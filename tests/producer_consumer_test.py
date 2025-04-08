import threading
import time
from typing import List

class ProducerConsumerTest:
    """
    Test harness that creates a single blocking producer and consumer
    using the MultiQueue interface. The producer adds items with delay,
    and the consumer removes them with a delay, simulating blocking behavior.
    """
    def __init__(
        self,
        queue,
        input_elements: List[int],
        producer_delay: float = 0.1,
        consumer_delay: float = 0.2,
    ):
        self.queue = queue
        self.input_elements = input_elements
        self.results: List[int] = []
        self.producer_delay = producer_delay
        self.consumer_delay = consumer_delay

    def producer(self):
        for item in self.input_elements:
            self.queue.add_item(item)
            time.sleep(self.producer_delay)

    def consumer(self):
        for _ in self.input_elements:
            item = self.queue.remove_item()
            self.results.append(item)
            time.sleep(self.consumer_delay)

    def run(self):
        producer_thread = threading.Thread(target=self.producer)
        consumer_thread = threading.Thread(target=self.consumer)

        producer_thread.start()
        consumer_thread.start()

        producer_thread.join()
        consumer_thread.join()

        return self.results
