import pytest

import queue

from processor import Processor
from context import Context


@pytest.fixture
def get_processor():
    def f(commands=None):
        processor_queue = queue.Queue()
        gui_data_queue = queue.Queue()

        processor = Processor(processor_queue, gui_data_queue)

        if commands is None:
            commands = []

        processor._commands = commands
        return processor
    return f


@pytest.fixture
def default_context():
    def f():
        context = Context()
        return context
    return f
