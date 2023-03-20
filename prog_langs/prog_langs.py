import pyautogui
import pyperclip

from prog_langs.base_prog_lang import BaseProgrammingLanguage

from utils import get_classes_in_module


class ProgrammingLanguageJava(BaseProgrammingLanguage):
    identifiers = ['java']
    name = 'Java'

    extensions = ['.java']

    def create_class(self, name):
        code = f'public class {name} {{\n\t\n}}'
        pyperclip.copy(code)
        pyautogui.hotkey('ctrl', 'v')

        return 1  # end line


class ProgrammingLanguagePython(BaseProgrammingLanguage):
    identifiers = ['python', 'py']
    name = 'Python'

    extensions = ['.py']


def get_prog_langs():
    return get_classes_in_module(__name__, subclass_of=BaseProgrammingLanguage)
