import datetime
import os
import time

import psutil
from confluent_kafka import Consumer


def print_current_memory_usage(len_messages):
    python_process = psutil.Process(os.getpid())
    process_memory = python_process.memory_info()[0] / 1024**2

    print(
        datetime.datetime.now(),
        "process memory: %.1f Mib" % (process_memory,),
        f"- messages processed: {len_messages}",
    )


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
