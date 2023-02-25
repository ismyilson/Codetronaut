from editors.base_editor import BaseEditor


class EditorVsCode(BaseEditor):
    def __init__(self):
        super().__init__()

        self.editor_name = 'Visual Studio Code'
        self.exe_name = 'Code.exe'

    def go_to_file(self, file_name):
        pass
