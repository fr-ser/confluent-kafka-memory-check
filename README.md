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

As all consumers behave the same way it stands to reason that the issue is with Python itself.

Confluent:

- The simple consumer takes about 20MB of memory in an idle state in the beginning.
- The memory during consuming a large backlog of messages increases (76MB).
- The memory goes down (46MB) after the backlog is processed, but it does not go back to the idle state.

Other consumers:

- AIOKafka behaves the same
- Kafka-Python behaves the same

## Outputs

### Confluent - Default settings

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

### Confluent - With additional settings to lower memory

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

### AIOKafka - default settings

```txt
2024-11-15 13:14:24.368988 process memory: 26.7 Mib - messages processed: 0
2024-11-15 13:14:26.372269 process memory: 26.8 Mib - messages processed: 0
2024-11-15 13:14:28.377425 process memory: 27.0 Mib - messages processed: 0
2024-11-15 13:14:29.668725 process memory: 27.0 Mib - messages processed: 1
2024-11-15 13:14:30.726755 process memory: 34.1 Mib - messages processed: 10000
2024-11-15 13:14:31.783996 process memory: 39.7 Mib - messages processed: 10000
2024-11-15 13:14:32.838416 process memory: 40.3 Mib - messages processed: 10000
2024-11-15 13:14:33.893997 process memory: 41.8 Mib - messages processed: 10000
2024-11-15 13:14:34.945454 process memory: 43.5 Mib - messages processed: 10000
2024-11-15 13:14:36.009189 process memory: 45.7 Mib - messages processed: 10000
2024-11-15 13:14:37.055374 process memory: 45.7 Mib - messages processed: 10000
2024-11-15 13:14:38.107253 process memory: 46.8 Mib - messages processed: 10000
2024-11-15 13:14:39.161762 process memory: 46.8 Mib - messages processed: 10000
2024-11-15 13:14:40.214951 process memory: 48.0 Mib - messages processed: 10000
2024-11-15 13:14:41.267444 process memory: 48.0 Mib - messages processed: 10000
2024-11-15 13:14:42.296582 process memory: 48.0 Mib - messages processed: 10000
2024-11-15 13:14:43.350355 process memory: 48.0 Mib - messages processed: 10000
2024-11-15 13:14:44.395915 process memory: 51.0 Mib - messages processed: 10000
2024-11-15 13:14:45.448427 process memory: 51.0 Mib - messages processed: 10000
2024-11-15 13:14:46.509665 process memory: 51.1 Mib - messages processed: 10000
2024-11-15 13:14:47.556084 process memory: 51.1 Mib - messages processed: 10000
2024-11-15 13:14:48.607270 process memory: 52.1 Mib - messages processed: 10000
2024-11-15 13:14:49.661793 process memory: 53.1 Mib - messages processed: 10000
2024-11-15 13:14:50.710564 process memory: 53.1 Mib - messages processed: 9999
2024-11-15 13:14:52.720750 process memory: 51.1 Mib - messages processed: 0
2024-11-15 13:14:54.726627 process memory: 51.1 Mib - messages processed: 0
2024-11-15 13:14:56.733809 process memory: 51.1 Mib - messages processed: 0
2024-11-15 13:14:58.738571 process memory: 51.1 Mib - messages processed: 0
2024-11-15 13:15:00.744128 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:02.747440 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:04.748915 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:06.754527 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:08.757089 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:10.760113 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:12.762348 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:14.763120 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:16.770059 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:18.775736 process memory: 51.2 Mib - messages processed: 0
2024-11-15 13:15:20.778798 process memory: 51.2 Mib - messages processed: 0
```

### KafkaPython - default settings

```txt
2024-11-15 13:47:21.083595 process memory: 26.7 Mib - messages processed: 0
2024-11-15 13:47:23.091339 process memory: 26.7 Mib - messages processed: 0
2024-11-15 13:47:25.097271 process memory: 26.7 Mib - messages processed: 0
2024-11-15 13:47:27.104497 process memory: 26.7 Mib - messages processed: 0
2024-11-15 13:47:28.195669 process memory: 35.6 Mib - messages processed: 10001
2024-11-15 13:47:29.286878 process memory: 40.9 Mib - messages processed: 10000
2024-11-15 13:47:30.383573 process memory: 40.2 Mib - messages processed: 10000
2024-11-15 13:47:31.472662 process memory: 44.3 Mib - messages processed: 10000
2024-11-15 13:47:32.552541 process memory: 49.0 Mib - messages processed: 10000
2024-11-15 13:47:33.644380 process memory: 50.1 Mib - messages processed: 10000
2024-11-15 13:47:34.730855 process memory: 50.1 Mib - messages processed: 10000
2024-11-15 13:47:35.825246 process memory: 51.2 Mib - messages processed: 10000
2024-11-15 13:47:36.912617 process memory: 51.3 Mib - messages processed: 10000
2024-11-15 13:47:38.002072 process memory: 51.3 Mib - messages processed: 10000
2024-11-15 13:47:39.082734 process memory: 53.4 Mib - messages processed: 10000
2024-11-15 13:47:40.168931 process memory: 53.4 Mib - messages processed: 10000
2024-11-15 13:47:41.260640 process memory: 53.5 Mib - messages processed: 10000
2024-11-15 13:47:42.345631 process memory: 53.8 Mib - messages processed: 10000
2024-11-15 13:47:43.433800 process memory: 55.3 Mib - messages processed: 10000
2024-11-15 13:47:44.523904 process memory: 55.3 Mib - messages processed: 10000
2024-11-15 13:47:45.608605 process memory: 55.4 Mib - messages processed: 10000
2024-11-15 13:47:46.698196 process memory: 55.4 Mib - messages processed: 10000
2024-11-15 13:47:47.785388 process memory: 55.4 Mib - messages processed: 10000
2024-11-15 13:47:48.867558 process memory: 55.4 Mib - messages processed: 9999
2024-11-15 13:47:50.878441 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:47:52.885425 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:47:54.893585 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:47:56.900658 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:47:58.908779 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:00.916687 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:02.919810 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:04.927758 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:06.931040 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:08.935686 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:10.943931 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:12.950100 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:14.953895 process memory: 55.4 Mib - messages processed: 0
2024-11-15 13:48:16.960845 process memory: 55.4 Mib - messages processed: 0
```

### AIOKafka - defaults with object graph

```txt
2024-11-21 14:53:42.743673 process memory: 29.7 Mib for PID 56358 - messages processed: 0
function                   5188
tuple                      3760
dict                       2706
ReferenceType              1619
wrapper_descriptor         1353
builtin_function_or_method 1089
method_descriptor          1037
getset_descriptor          868
type                       824
cell                       758

...

2024-11-21 14:54:32.768141 process memory: 60.3 Mib for PID 56358 - messages processed: 10000
ConsumerRecord             10000
function                   5186
tuple                      3581
dict                       2625
ReferenceType              1637
wrapper_descriptor         1353
builtin_function_or_method 1106
method_descriptor          1037
getset_descriptor          868
type                       824

...

2024-11-21 14:54:54.044112 process memory: 58.3 Mib for PID 56358 - messages processed: 0
function                   5188
tuple                      3587
dict                       2624
ReferenceType              1637
wrapper_descriptor         1353
builtin_function_or_method 1107
method_descriptor          1037
getset_descriptor          868
type                       824
cell                       758
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
