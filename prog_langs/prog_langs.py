from prog_langs.base_prog_lang import BaseProgrammingLanguage

from utils import get_classes_in_module


class ProgrammingLanguageJava(BaseProgrammingLanguage):
    identifiers = ['java']
    name = 'Java'

    extensions = ['.java']


class ProgrammingLanguagePython(BaseProgrammingLanguage):
    identifiers = ['python', 'py']
    name = 'Python'

    extensions = ['.py']


def get_prog_langs():
    return get_classes_in_module(__name__, subclass_of=BaseProgrammingLanguage)
