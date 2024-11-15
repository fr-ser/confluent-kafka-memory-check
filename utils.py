import datetime
import os

import psutil


def print_current_memory_usage(len_messages):
    python_process = psutil.Process(os.getpid())
    process_memory = python_process.memory_info()[0] / 1024**2

    print(
        datetime.datetime.now(),
        "process memory: %.1f Mib" % (process_memory,),
        f"- messages processed: {len_messages}",
    )
