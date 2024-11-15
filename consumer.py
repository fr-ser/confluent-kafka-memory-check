import time

from confluent_kafka import Consumer

from utils import print_current_memory_usage


def main():
    consumer = Consumer(
        {
            "group.id": "test-consumer",
            "bootstrap.servers": "localhost:9092",
            # "queued.min.messages": 1,
            # "queued.max.messages.kbytes": 3_000,
            # "fetch.max.bytes": 3_000_000,
        }
    )

    consumer.subscribe(["test-topic"])

    try:
        while True:
            messages = consumer.consume(num_messages=15_000, timeout=1.0)
            print_current_memory_usage(len(messages))
            time.sleep(1)  # simulating some processing time

    finally:
        consumer.close()


if __name__ == "__main__":
    main()
