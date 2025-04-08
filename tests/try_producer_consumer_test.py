import time
import threading
from src.multi_queue import MultiQueue

class TryProducerConsumerTest:
    def __init__(self, queue: MultiQueue, input_data: list):
        self.queue = queue
        self.input_data = input_data
        self.produced = []
        self.consumed = []

    def run(self):
        def producer():
            for item in self.input_data:
                while not self.queue.try_add_item(item):
                    time.sleep(0.01)
                self.produced.append(item)

        def consumer():
            while len(self.consumed) < len(self.input_data):
                item = self.queue.try_remove_item()
                if item is not None:
                    self.consumed.append(item)
                else:
                    time.sleep(0.01)

        pt = threading.Thread(target=producer)
        ct = threading.Thread(target=consumer)
        pt.start()
        ct.start()
        pt.join()
        ct.join()

        return self.produced, self.consumed
