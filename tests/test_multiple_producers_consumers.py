import threading
from src.multi_queue import MultiQueue

def test_two_producers_two_consumers_even_split():
    """
    Test multi-threaded producer-consumer coordination with 2 producers,
    2 consumers, and even split of total items to ensure safe and complete consumption.
    """
    queue = MultiQueue(4)
    input_sets, total_items = _create_input_sets()

    producers = _start_producers(queue, input_sets)

    consumed = []
    consumed_lock = threading.Lock()
    consumers = _start_consumers(queue, total_items, consumed, consumed_lock)

    for t in producers + consumers:
        t.join()

    assert sorted(consumed) == sorted(sum(input_sets, []))

def _create_input_sets() -> tuple[list[list[int]], int]:
    # Two producers, each with 3 items = total 6 (even)
    input_sets = [
        [1, 2, 3],
        [4, 5, 6],
    ]
    total_items = sum(len(s) for s in input_sets)
    assert total_items % 2 == 0, "This test assumes even total items"

    return input_sets, total_items

def _start_producers(
    queue, 
    input_sets: list[list[int]]
) -> list[threading.Thread]:
    def producer(input_data):
        for item in input_data:
            queue.add_item(item)

    producers = [threading.Thread(target=producer, args=(data,)) for data in input_sets]
    for t in producers:
        t.start()

    return producers

def _start_consumers(
    queue, 
    total_items: int, 
    consumed: list[int], 
    consumed_lock: threading.Lock
) -> list[threading.Thread]:
    def consumer(consume_count: int):
        for _ in range(consume_count):
            item = queue.remove_item()
            with consumed_lock:
                consumed.append(item)

    consume_count = total_items // 2 # evenly split
    consumers = [threading.Thread(target=consumer, args=(consume_count,)) for _ in range(2)]
    for t in consumers:
        t.start()

    return consumers
