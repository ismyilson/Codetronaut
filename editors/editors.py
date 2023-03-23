import writer as wr

from editors.base_editor import BaseEditor
from utils import get_classes_in_module


def get_editors():
    return get_classes_in_module(__name__, subclass_of=BaseEditor)


class EditorVisualStudioCode(BaseEditor):
    identifiers = ['vscode', 'visualstudiocode']
    name = 'Visual Studio Code'
    exe_name = 'Code.exe'

    def go_to_file(self, file):
        writer = wr.Writer()

        writer.add_hotkey('ctrl+p')
        writer.add_text(file)
        writer.add_hotkey('enter')

        writer.execute()

    def go_to_line(self, line, col=10000):
        line = str(line)
        col = str(col)

        writer = wr.Writer()

        writer.add_hotkey('ctrl+g')
        writer.add_text(f'{line}:{col}')
        writer.add_hotkey('enter')

        writer.execute()

    def save_file(self):
        writer = wr.Writer()

        writer.add_hotkey('ctrl+s')

        writer.execute()

    def save_all_files(self):
        writer = wr.Writer()

        writer.add_hotkey('ctrl+k')
        writer.add_hotkey('s')

        writer.execute()

    def delete_lines(self, line_start, line_end):
        line_start = str(line_start)
        line_end = str(line_end)


