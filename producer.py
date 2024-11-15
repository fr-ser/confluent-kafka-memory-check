from confluent_kafka import Producer


def main():
    producer = Producer({"bootstrap.servers": "localhost:9092"})

    for index in range(200_000):
        producer.produce(
            topic="test-topic",
            value=f"random value with some text and an index of {index}",
        )
        if index % 10_000 == 0:
            producer.flush(0.1)
    producer.flush()
    print("Done")


if __name__ == "__main__":
    main()
