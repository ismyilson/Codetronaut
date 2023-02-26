import pyautogui

from editors.base_editor import BaseEditor
from handlers import win_handler


class EditorVsCode(BaseEditor):
    HOTKEYS = {
        'gotofile': [
            'ctrl',
            'p'
        ]
    }

    def __init__(self):
        super().__init__()

        self.editor_name = 'Visual Studio Code'
        self.exe_name = 'Code.exe'

    def go_to_file(self, file_name):
        super().go_to_file(file_name)

        pyautogui.hotkey(*self.HOTKEYS['gotofile'])

        pyautogui.write(file_name)
        pyautogui.press('enter')
        return True
