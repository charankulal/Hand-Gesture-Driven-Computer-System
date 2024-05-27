import time
from datetime import datetime


class CountsPerSec:
    """
    Class that tracks the number of occurrences ("counts") of an
    arbitrary event and returns the frequency in occurrences
    (counts) per second. The caller must increment the count.
    """

    def __init__(self):
        self._start_time = None
        self._num_occurrences = 0
        self._prev_occurrences = 0
        self._fps_time = None
        self._fps_gap = 0
        self._fps = 0

    def start(self):
        self._start_time = datetime.now()
        self._fps_time = time.time()
        return self

    def increment(self):
        self._num_occurrences += 1
        if time.time() - self._fps_time >= 1:
            # print("1 sec")
            self._fps = self._num_occurrences - self._prev_occurrences
            self._fps_time = time.time()
            self._prev_occurrences = self._num_occurrences

        # self._fps = 1/self._fps_gap

    def countsPerSec(self):
        elapsed_time = (datetime.now() - self._start_time).total_seconds()
        try:
            return self._num_occurrences / elapsed_time
        except ZeroDivisionError:
            return 0

    def countsPerSecNow(self):
        return self._fps
