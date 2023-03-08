from audio import reader

from handlers import win_handler


class Editor:
    editor_name: str
    exe_name: str
    pid: int

    hotkeys: dict

    def __init__(self):
        self.editor_name = ''
        self.exe_name = ''
        self.pid = -1

        self.hotkeys = dict()

    def run(self, workdir):
        reader.read_text('Launching editor')

        process = win_handler.run(self.editor_name, self.exe_name, workdir=workdir)

        if process is None:
            return

        self.pid = process.pid

    def is_running(self):
        return win_handler.process_is_running(self.exe_name)

    def create_file(self, full_path):
        try:
            win_handler.create_file(full_path)
            return True
        except FileExistsError:
            return False

    def go_to_file(self, file_name):
        return False

    def close(self):
        if self.is_running():
            win_handler.close_process(self.pid)