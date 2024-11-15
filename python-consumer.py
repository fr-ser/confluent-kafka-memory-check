import time

from kafka import KafkaConsumer

from utils import print_current_memory_usage


def main():
    consumer = KafkaConsumer(
        "test-topic", bootstrap_servers="localhost:9092", group_id="test-group-python"
    )
    try:
        while True:
            result = consumer.poll(timeout_ms=1_000, max_records=15_000)
            print_current_memory_usage(sum(len(item[1]) for item in result.items()))
            time.sleep(1)  # simulating some processing time
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
