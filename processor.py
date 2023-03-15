import threading

from queue import Queue

from global_vars import t_event_record


class Processor(threading.Thread):
    _queue: Queue
    _gui_data_queue: Queue

    def __init__(self, processor_queue, gui_data_queue):
        super().__init__(daemon=True)

        self._queue = processor_queue
        self._gui_data_queue = gui_data_queue

    def _loop(self):
        while True:
            user_input = self._queue.get()

            self._gui_data_queue.put(('-TRANSCRIBEDTEXT-', user_input.raw_text))

            t_event_record.set()

    def run(self):
        self._loop()
