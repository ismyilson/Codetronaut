from threading import Lock

from os import path

from editors.editor import Editor
from user_platform.user_platform import UserPlatform
from programming_language.programming_language import ProgrammingLanguage

CONTEXT_SAVE_PATH = path.expandvars(r'%LOCALAPPDATA%\Voice2Code\context')


class SingletonMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Context(metaclass=SingletonMeta):
    editor: Editor
    platform: UserPlatform
    programming_language: ProgrammingLanguage

    work_directory: str

    current_directory: str

    def __init__(self):
        pass
