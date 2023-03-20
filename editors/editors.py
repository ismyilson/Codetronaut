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
