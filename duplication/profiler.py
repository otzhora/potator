import atexit
from collections import defaultdict
import os
import time

DEBUG = os.getenv("DEBUG", None) is not None
DEBUG_COUNTS = defaultdict(int)
DEBUG_TIMES = defaultdict(float)


def print_debug_exit():
    if DEBUG:
        for name, _ in sorted(DEBUG_TIMES.items(), key=lambda x: -x[1]):
            print(f"{name:>50} : {DEBUG_COUNTS[name]:>6} {DEBUG_TIMES[name]:>10.2f} ms")


atexit.register(print_debug_exit)


class Profile:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        if DEBUG:
            self.st = time.time()

    def __exit__(self, *junk):
        if DEBUG:
            et = (time.time() - self.st) * 1000

            DEBUG_COUNTS[self.name] += 1
            DEBUG_TIMES[self.name] += et
