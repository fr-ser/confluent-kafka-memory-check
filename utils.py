import datetime
import os

import objgraph
import psutil


def print_current_memory_usage(len_messages, show_object_graph=False):
    python_process = psutil.Process(os.getpid())
    process_memory = python_process.memory_info()[0] / 1024**2

    print(
        datetime.datetime.now(),
        "process memory: %.1f Mib for PID %s" % (process_memory, os.getpid()),
        f"- messages processed: {len_messages}",
    )
    if show_object_graph:
        objgraph.show_most_common_types()
