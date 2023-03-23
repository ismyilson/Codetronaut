import pyautogui

from editors.base_editor import BaseEditor
from utils import get_classes_in_module


def get_editors():
    return get_classes_in_module(__name__, subclass_of=BaseEditor)


class EditorVisualStudioCode(BaseEditor):
    identifiers = ['vscode', 'visualstudiocode']
    name = 'Visual Studio Code'
    exe_name = 'Code.exe'

    def go_to_file(self, file):
        pyautogui.hotkey('ctrl', 'p')

        pyautogui.write(file)
        pyautogui.press('enter')

    def go_to_line(self, line, col=10000):
        line = str(line)
        col = str(col)

        pyautogui.hotkey('ctrl', 'g')

        pyautogui.write(f'{line}:{col}')
        pyautogui.press('enter')

    def save_file(self):
        pyautogui.hotkey('ctrl', 's')

    def save_all_files(self):
        pyautogui.hotkey('ctrl', 'shift', 's')
