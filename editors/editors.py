import writer as wr

from editors.base_editor import BaseEditor
from utils import get_classes_in_module

from pynput.keyboard import Key


def get_editors():
    return get_classes_in_module(__name__, subclass_of=BaseEditor)


class EditorVisualStudioCode(BaseEditor):
    identifiers = ['vscode', 'visualstudiocode']
    name = 'Visual Studio Code'
    exe_name = 'Code.exe'

    def go_to_file(self, file):
        writer = wr.Writer()

        writer.add_hotkey([Key.ctrl_l, 'p'])
        writer.add_text(file)
        writer.add_key(Key.enter)

        writer.execute()

    def go_to_line(self, line, column=10000):
        line = str(line)
        column = str(column)

        writer = wr.Writer()

        writer.add_hotkey([Key.ctrl_l, 'g'])
        writer.add_text(f'{line}:{column}')
        writer.add_key(Key.enter)

        writer.execute()

    def save_file(self):
        writer = wr.Writer()

        writer.add_hotkey([Key.ctrl_l, 's'])

        writer.execute()

    def save_all_files(self):
        writer = wr.Writer()

        writer.add_hotkey([Key.ctrl_l, 'k'])
        writer.add_key('s')

        writer.execute()

    def refactor_rename(self, new_name):
        writer = wr.Writer()

        writer.add_key(Key.f2)
        writer.add_text(new_name)
        writer.add_key(Key.enter)

        writer.execute()

    def select_line(self, line):
        self.go_to_line(line)

        writer = wr.Writer()

        writer.add_hotkey([Key.shift, Key.home])

        writer.execute()
