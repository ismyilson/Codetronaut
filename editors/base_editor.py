import abc

import pyautogui


class UnsupportedEditor(Exception):
    def __init__(self, message):
        super().__init__(message)


class BaseEditor(abc.ABC):
    identifiers: list[str]
    name: str
    exe_name: str

    def new_line(self):
        pyautogui.press('enter')

    def go_to_file(self, file):
        pass

    def go_to_line(self, line):
        pass

    def save_file(self):
        pass
