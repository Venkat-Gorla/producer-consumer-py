# Producer-Consumer with MultiQueue (Python)

This project implements a thread-safe bounded queue (`MultiQueue`) that supports the classic **Producer-Consumer problem**, where:

- Producers must wait when the queue is full.
- Consumers must wait when the queue is empty.
- All synchronization must be handled internally using Python's threading primitives.

## ✅ Features

✔️ Monitor-style synchronization using `threading.Condition`  
✔️ Mutual exclusion across producers and consumers  
✔️ Blocking and non-blocking APIs:  
  - `add_item()`, `remove_item()` (blocking)  
  - `try_add_item()`, `try_remove_item()` (non-blocking)  

✔️ Fully tested with comprehensive unit test coverage  

## 📊 Design Overview

- Internally uses a `deque` to hold items.
- A shared `Lock` underlies two condition variables:
  - `not_full` (used by producers)
  - `not_empty` (used by consumers)
- Condition signaling ensures threads only proceed when it's safe to do so.

## 🗂️ Project Structure

```
producer-consumer-py/
├── src/
│   └── multi_queue.py                       # MultiQueue class implementation
├── tests/
│   ├── test_single_producer_consumer.py     # Blocking and non-blocking test: single producer-consumer
│   ├── test_multiple_producers_consumers.py # Blocking test: multiple producers/consumers
│   ├── producer_consumer_test.py            # Blocking test harness class
│   ├── try_producer_consumer_test.py        # Non-blocking test harness class
├── pytest.ini
└── README.md
```

## 🧪 Unit Testing

- Tests written using `pytest`
- Both blocking and non-blocking interfaces are covered
- Coordination done via `threading.Event`, `Locks`, and deterministic test harnesses

### Sample tests:

- Single producer/consumer using blocking queue with delays
- Deterministic coordination using `Event` instead of `sleep`
- Try-based coordination without blocking using retry loops
- Multi-producer and multi-consumer test with even split and lock-safe appending

### To run the tests:

```bash
pytest
```
## ✅ Unit Tests in Action

Will be added soon

## 🚀 Usage

```python
from src.multi_queue import MultiQueue

queue = MultiQueue(capacity=3)
queue.add_item(10)           # Blocking add
item = queue.remove_item()   # Blocking remove

queue.try_add_item(20)       # Non-blocking add
queue.try_remove_item()      # Non-blocking remove
```

## 🔍 Future Improvements

- Timeout support for `add_item()` and `remove_item()`
- Metrics for wait time or queue occupancy
- Support for item prioritization

## 👨‍💻 About the Author

I'm a seasoned software developer who built this project out of personal interest to explore and deepen my understanding of **Python concurrency and synchronization**. This implementation focuses on correctness, determinism, and clean architecture — reflecting real-world concurrent programming scenarios.

---

Made with ❤️ using threads and clean code.
