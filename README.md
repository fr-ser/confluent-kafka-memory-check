# Investigation - Memory Usage of Confluent Kafka

This investigation was about a Confluent Kafka consumer not releasing memory after hitting a message spike.

## Setup

- install Docker (and docker compose)
- install Python
- install poetry (to make an isolated/virtual python environment and install packages)
- install python packages: `poetry install --no-root`
- start kafka: `docker compose up -d --wait`
- run the consumer: `poetry run python consumer.py`
- add data to kafka: `poetry run python producer.py` (in a separate terminal)

## Observations

The observations are based on the output below.

- The simple consumer takes about 20MB of memory in an idle state in the beginning.
- The memory during consuming a large backlog of messages increases (76MB).
- The memory goes down (46MB) after the backlog is processed, but it does not go back to the idle state.

## Outputs

### Default settings

```txt
2024-11-15 12:58:53.861962 process memory: 19.4 Mib - messages processed: 0
2024-11-15 12:58:55.871964 process memory: 19.5 Mib - messages processed: 0
2024-11-15 12:58:57.876081 process memory: 19.8 Mib - messages processed: 0
2024-11-15 12:58:59.886247 process memory: 19.9 Mib - messages processed: 0
2024-11-15 12:59:00.935911 process memory: 30.4 Mib - messages processed: 15000
2024-11-15 12:59:01.949484 process memory: 61.7 Mib - messages processed: 15000
2024-11-15 12:59:02.970987 process memory: 65.6 Mib - messages processed: 15000
2024-11-15 12:59:03.993949 process memory: 71.7 Mib - messages processed: 15000
2024-11-15 12:59:05.012300 process memory: 71.6 Mib - messages processed: 15000
2024-11-15 12:59:06.034214 process memory: 76.2 Mib - messages processed: 15000
2024-11-15 12:59:07.047438 process memory: 73.8 Mib - messages processed: 15000
2024-11-15 12:59:08.068643 process memory: 74.3 Mib - messages processed: 15000
2024-11-15 12:59:09.089038 process memory: 72.3 Mib - messages processed: 15000
2024-11-15 12:59:10.109189 process memory: 70.5 Mib - messages processed: 15000
2024-11-15 12:59:11.130012 process memory: 63.6 Mib - messages processed: 15000
2024-11-15 12:59:12.141301 process memory: 60.6 Mib - messages processed: 15000
2024-11-15 12:59:13.163147 process memory: 54.7 Mib - messages processed: 15000
2024-11-15 12:59:15.181563 process memory: 52.9 Mib - messages processed: 5000
2024-11-15 12:59:17.188381 process memory: 45.9 Mib - messages processed: 0
2024-11-15 12:59:19.198570 process memory: 45.9 Mib - messages processed: 0
2024-11-15 12:59:21.209367 process memory: 45.9 Mib - messages processed: 0
2024-11-15 12:59:23.217975 process memory: 45.9 Mib - messages processed: 0
2024-11-15 12:59:25.226659 process memory: 45.9 Mib - messages processed: 0
2024-11-15 12:59:27.233276 process memory: 45.9 Mib - messages processed: 0
2024-11-15 12:59:29.238706 process memory: 45.9 Mib - messages processed: 0
```

### With additional settings to lower memory

Adding these settings

```txt
"queued.min.messages": 1,
"queued.max.messages.kbytes": 3_000,
"fetch.max.bytes": 3_000_000,
````

Result:

```txt
2024-11-15 13:01:25.313715 process memory: 19.5 Mib - messages processed: 0
2024-11-15 13:01:27.324493 process memory: 19.7 Mib - messages processed: 0
2024-11-15 13:01:29.329229 process memory: 19.7 Mib - messages processed: 0
2024-11-15 13:01:31.335069 process memory: 20.0 Mib - messages processed: 0
2024-11-15 13:01:32.871542 process memory: 27.7 Mib - messages processed: 15000
2024-11-15 13:01:34.882079 process memory: 28.7 Mib - messages processed: 3140
2024-11-15 13:01:36.901409 process memory: 30.2 Mib - messages processed: 11861
2024-11-15 13:01:37.946572 process memory: 36.4 Mib - messages processed: 15000
2024-11-15 13:01:39.959274 process memory: 33.9 Mib - messages processed: 5000
2024-11-15 13:01:41.977985 process memory: 34.1 Mib - messages processed: 10000
2024-11-15 13:01:43.995478 process memory: 35.7 Mib - messages processed: 10000
2024-11-15 13:01:45.032254 process memory: 41.9 Mib - messages processed: 15000
2024-11-15 13:01:47.045435 process memory: 40.9 Mib - messages processed: 5000
2024-11-15 13:01:49.063907 process memory: 41.0 Mib - messages processed: 10000
2024-11-15 13:01:51.078799 process memory: 42.2 Mib - messages processed: 10000
2024-11-15 13:01:52.126432 process memory: 47.2 Mib - messages processed: 15000
2024-11-15 13:01:54.138320 process memory: 47.2 Mib - messages processed: 5000
2024-11-15 13:01:56.150669 process memory: 46.2 Mib - messages processed: 10000
2024-11-15 13:01:57.193106 process memory: 49.2 Mib - messages processed: 15000
2024-11-15 13:01:59.215211 process memory: 46.8 Mib - messages processed: 15000
2024-11-15 13:02:01.225256 process memory: 39.9 Mib - messages processed: 0
2024-11-15 13:02:03.244365 process memory: 41.5 Mib - messages processed: 10000
2024-11-15 13:02:05.264133 process memory: 45.2 Mib - messages processed: 10000
2024-11-15 13:02:07.286656 process memory: 44.5 Mib - messages processed: 9999
2024-11-15 13:02:09.296021 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:11.302333 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:13.311907 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:15.321001 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:17.327686 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:19.336823 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:21.346633 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:23.356637 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:25.366611 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:27.375520 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:29.385831 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:31.393113 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:33.397541 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:35.406112 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:37.413001 process memory: 41.5 Mib - messages processed: 0
2024-11-15 13:02:39.423278 process memory: 41.5 Mib - messages processed: 0
```

## Helpful commands

These commands assume the kafka-cli to be installed

Check topic offset:
`kafka-run-class org.apache.kafka.tools.GetOffsetShell --broker-list http://localhost:9092 --topic test-topic`

Check consumer group:
`kafka-consumer-groups --bootstrap-server http://localhost:9092  --describe --group test-consumer`

Change offset:

- to-earliest:
`kafka-consumer-groups --bootstrap-server http://localhost:9092 --group test-consumer --reset-offsets --topic test-topic --to-earliest --execute`

- to-latest:
`kafka-consumer-groups --bootstrap-server http://localhost:9092 --group test-consumer --reset-offsets --topic test-topic --to-latest --execute`

- shift:
`kafka-consumer-groups --bootstrap-server http://localhost:9092 --group test-consumer --reset-offsets --topic test-topic --shift-by -15000 --execute`
