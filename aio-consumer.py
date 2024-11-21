import asyncio
import time

from aiokafka import AIOKafkaConsumer

from utils import print_current_memory_usage


async def consume():
    consumer = AIOKafkaConsumer(
        "test-topic",
        bootstrap_servers="localhost:9092",
        group_id="test-group-aio",
    )
    await consumer.start()
    try:
        while True:
            result = await consumer.getmany(timeout_ms=1_000, max_records=15_000)
            print_current_memory_usage(
                sum(len(item[1]) for item in result.items()), True
            )
            time.sleep(1)  # simulating some processing time
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
