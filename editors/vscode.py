from editors.base import BaseEditor

from handlers.win_handler import open_process


class EditorVsCode(BaseEditor):
    def __init__(self):
        super().__init__()

        self.editor_name = 'vscode'
        self.process_name = 'code'

    def run(self, workdir):
        super().run(workdir)

        process = open_process(self.process_name, workdir=workdir)

    def go_to_file(self, file_name):
        pass
