import queue

from input_handling.audio_recorder import AudioRecorder
from global_vars import t_event_record, t_event_not_muted
from processor import Processor
from gui import GUI


class App:
    processor_queue: queue.Queue
    gui_data_queue: queue.Queue

    _audio_recorder: AudioRecorder
    _processor: Processor
    _gui: GUI

    def start(self):
        self._init_queues()

        self._setup_threads()
        self._setup_gui()

        self._start_threads()

        self._start_gui()

    def _init_queues(self):
        self.processor_queue = queue.Queue()
        self.gui_data_queue = queue.Queue()

    def _setup_threads(self):
        self._audio_recorder = AudioRecorder(self.processor_queue)
        self._processor = Processor(self.processor_queue, self.gui_data_queue)

    def _start_threads(self):
        self._audio_recorder.start()
        self._processor.start()

        t_event_record.set()
        t_event_not_muted.set()

    def _setup_gui(self):
        self._gui = GUI(self.gui_data_queue)

    def _start_gui(self):
        self._gui.start()

        self._audio_recorder.join()
        self._processor.join()


if __name__ == '__main__':
    application = App()
    application.start()
