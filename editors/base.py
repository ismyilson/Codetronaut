import reader
from handlers.win_handler import process_is_running


class BaseEditor:
    editor_name: str
    process_name: str

    def __init__(self):
        self.editor_name = ''
        self.process_name = ''

    def run(self, workdir):
        reader.read_text('Launching editor')

    def is_running(self):
        return process_is_running(self.process_name)

    def go_to_file(self, file_name):
        pass
